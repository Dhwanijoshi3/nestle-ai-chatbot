# app.py - Optimized FastAPI for Azure with lazy-loading

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI instance
app = FastAPI(title="Nestlé AI Chatbot", version="1.0.0")

# Globals for lazy init
G = None
node_embeddings = None
graph_built = False

GRAPH_DIR = "graph"
LOG_DIR = "logs"
GRAPH_FILE = os.path.join(GRAPH_DIR, "graph.pkl")

# Ensure necessary directories
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Pydantic model
class Query(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    print("✅ App startup event triggered (lightweight)")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "graph_exists": os.path.exists(GRAPH_FILE),
        "graph_loaded": G is not None,
        "nodes_count": G.number_of_nodes() if G else 0,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/chat")
def chat(query: Query):
    global G, node_embeddings, graph_built
    from backend.retriever import load_graph, embed_nodes, get_top_nodes
    from backend.openai_interface import ask_openai
    from backend.web_scraper import scrape_web, get_fallback_nestle_urls

    try:
        print(f"[DEBUG] Received query: {query.question}")

        # Build graph if missing
        if not os.path.exists(GRAPH_FILE):
            print("📊 graph.pkl not found, building...")
            from backend.graph_builder import build_graph
            build_graph()
            graph_built = True

        # Load graph + embeddings lazily
        if G is None or node_embeddings is None:
            G = load_graph()
            node_embeddings = embed_nodes(G)
            print(f"✅ Loaded graph with {G.number_of_nodes()} nodes")

        # Get graph context
        try:
            top_nodes = get_top_nodes(query.question, G, node_embeddings, k=5)
            graph_context = "\n".join(
                f"**{node}**: {G.nodes[node]['description']}"
                for node in top_nodes if node in G.nodes
            )
        except Exception as e:
            print(f"[Fallback] Graph error: {e}")
            graph_context = get_basic_nestle_context(query.question)

        # Web scrape
        try:
            web_results = scrape_web(query.question, num_results=5)
            if not web_results:
                web_results = get_fallback_nestle_urls(query.question)
        except Exception as e:
            print(f"[Fallback] Web scrape failed: {e}")
            web_results = get_fallback_nestle_urls(query.question)

        web_context = "\n".join([f"- {url}" for url in web_results])
        full_context = f"""NESTLÉ KNOWLEDGE BASE:
{graph_context}

RELEVANT NESTLÉ WEBSITES:
{web_context}

QUERY CONTEXT: {query.question}
Please respond about Nestlé Canada products/services only."""

        # AI Response
        try:
            answer = ask_openai(query.question, full_context)
        except Exception as e:
            print(f"[Fallback] AI error: {e}")
            answer = get_emergency_fallback_response(query.question)

        return {
            "answer": answer,
            "sources": web_results or []
        }

    except Exception as e:
        print(f"[ERROR] Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_basic_nestle_context(query):
    q = query.lower()
    context = "**Nestlé Canada**: Leading food and beverage company with KitKat, Smarties, Aero, Coffee-mate, and more.\n"
    if any(word in q for word in ["chocolate", "sweet"]):
        context += "**Chocolates**: KitKat, Aero, Smarties, Quality Street.\n"
    if any(word in q for word in ["coffee", "beverage"]):
        context += "**Beverages**: Coffee-mate, Nespresso, Carnation.\n"
    if any(word in q for word in ["nutrition", "baby"]):
        context += "**Nutrition**: Gerber baby food, Carnation milk.\n"
    if any(word in q for word in ["sustainability", "environment"]):
        context += "**Sustainability**: Ethical cocoa, water stewardship.\n"
    if any(word in q for word in ["holiday", "gift"]):
        context += "**Holiday**: Advent calendars, gift boxes.\n"
    context += "**Values**: 'Good Food, Good Life', Canadian made."
    return context

def get_emergency_fallback_response(query):
    return """Hi! I'm your Nestlé Canada assistant.
Our brands include:
- KitKat
- Smarties
- Aero
- Coffee-mate
- Quality Street

Visit **madewithnestle.ca** for more.

How can I help today?"""

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def get_ui():
    return FileResponse(os.path.join("frontend", "index.html"))

# Entrypoint
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=os.getenv("DEBUG", "False") == "true")
