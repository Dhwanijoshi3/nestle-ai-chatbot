# # app.py - Main application file for Azure deployment

# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# import os
# import uvicorn
# from dotenv import load_dotenv
# #from dotenv import load_dotenv

# # ✅ Insert startup logic here
# # ----- Minimal Azure Free-compatible startup logic -----
# GRAPH_DIR = "graph"
# LOG_DIR = "logs"
# GRAPH_FILE = os.path.join(GRAPH_DIR, "graph.pkl")

# os.makedirs(GRAPH_DIR, exist_ok=True)
# os.makedirs(LOG_DIR, exist_ok=True)

# if not os.path.exists(GRAPH_FILE):
#     print("📊 graph.pkl not found — building knowledge graph...")
#     try:
#         from backend.graph_builder import build_graph
#         build_graph()
#         print("✅ Knowledge graph built successfully.")
#     except Exception as e:
#         print(f"❌ Error building graph: {e}")
# else:
#     print("✅ graph.pkl already exists — skipping build.")
# # --------------------------------------------------------

# #app = FastAPI(title="Nestlé AI Chatbot", version="1.0.0")

# # Import your modules from backend folder
# from backend.retriever import load_graph, embed_nodes, get_top_nodes
# from backend.openai_interface import ask_openai
# from backend.web_scraper import scrape_web, get_fallback_nestle_urls

# # Load environment variables
# load_dotenv()

# app = FastAPI(title="Nestlé AI Chatbot", version="1.0.0")

# # Global variables for graph and embeddings
# G = None
# node_embeddings = None

# @app.on_event("startup")
# async def startup_event():
#     """Initialize the application on startup"""
#     global G, node_embeddings
    
#     print("🚀 Starting Nestlé AI Chatbot...")
    
#     # Try to load graph and embeddings
#     try:
#         print("📊 Loading knowledge graph...")
#         G = load_graph()
#         node_embeddings = embed_nodes(G)
#         print(f"✅ Graph loaded successfully with {G.number_of_nodes()} nodes")
#     except Exception as e:
#         print(f"⚠️ Warning: Could not load graph: {e}")
#         print("📝 Building new graph...")
#         try:
#             from backend.graph_builder import build_graph
#             build_graph()
#             G = load_graph()
#             node_embeddings = embed_nodes(G)
#             print(f"✅ New graph built with {G.number_of_nodes()} nodes")
#         except Exception as build_error:
#             print(f"❌ Error building graph: {build_error}")
#             G = None
#             node_embeddings = None
    
#     print("🎉 Nestlé AI Chatbot is ready!")

# # Pydantic model for incoming JSON
# class Query(BaseModel):
#     question: str

# # Health check endpoint
# @app.get("/health")
# def health_check():
#     """Health check endpoint for Azure App Service"""
#     return {
#         "status": "healthy",
#         "graph_loaded": G is not None,
#         "nodes_count": G.number_of_nodes() if G else 0,
#         "environment": os.getenv("ENVIRONMENT", "development")
#     }

# # Main chat endpoint
# @app.post("/chat")
# def chat(query: Query):
#     """Main chat endpoint that processes user queries"""
#     try:
#         print(f"[DEBUG] Received query: {query.question}")
        
#         # Get graph context if available
#         graph_context = ""
#         if G and node_embeddings:
#             try:
#                 top_nodes = get_top_nodes(query.question, G, node_embeddings, k=5)
#                 graph_context = "\n".join([
#                     f"**{node}**: {G.nodes[node]['description']}" 
#                     for node in top_nodes if node in G.nodes
#                 ])
#                 print(f"[DEBUG] Top graph nodes: {top_nodes}")
#             except Exception as e:
#                 print(f"[DEBUG] Graph retrieval error: {e}")
#                 graph_context = get_basic_nestle_context(query.question)
#         else:
#             graph_context = get_basic_nestle_context(query.question)
        
#         # Get web results with improved scraper
#         web_results = []
#         try:
#             web_results = scrape_web(query.question, num_results=5)
#             print(f"[DEBUG] Web results found: {len(web_results)}")
            
#             # If no web results, use fallback URLs
#             if not web_results:
#                 web_results = get_fallback_nestle_urls(query.question)
#                 print(f"[DEBUG] Using fallback URLs: {len(web_results)}")
                
#         except Exception as e:
#             print(f"[DEBUG] Web scraping error: {e}")
#             web_results = get_fallback_nestle_urls(query.question)
        
#         # Create comprehensive context
#         web_context = "\n".join([f"- {url}" for url in web_results]) if web_results else ""
        
#         full_context = f"""NESTLÉ KNOWLEDGE BASE:
# {graph_context}

# RELEVANT NESTLÉ WEBSITES:
# {web_context}

# QUERY CONTEXT: The user is asking about: {query.question}
# Please provide a response specifically focused on Nestlé Canada products, services, and information."""

#         print(f"[DEBUG] Context length: {len(full_context)}")
        
#         # Get AI response
#         try:
#             answer = ask_openai(query.question, full_context)
#             print(f"[DEBUG] AI response generated successfully")
#         except Exception as e:
#             print(f"[DEBUG] AI response error: {e}")
#             answer = get_emergency_fallback_response(query.question)
        
#         return {
#             "answer": answer,
#             "sources": web_results or []
#         }
    
#     except Exception as e:
#         print(f"[ERROR] Chat endpoint error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# def get_basic_nestle_context(query):
#     """Provide basic Nestlé context when graph is not available"""
#     query_lower = query.lower()
    
#     context = "**Nestlé Canada**: Leading food and beverage company with brands like KitKat, Smarties, Aero, Coffee-mate, and Quality Street.\n"
    
#     if any(word in query_lower for word in ["chocolate", "candy", "sweet"]):
#         context += "**Chocolate Brands**: KitKat wafer bars, Smarties colorful chocolates, Aero bubbly chocolate, Quality Street assorted chocolates.\n"
    
#     if any(word in query_lower for word in ["coffee", "beverage", "drink"]):
#         context += "**Beverages**: Nespresso premium coffee, Coffee-mate creamers, Carnation hot chocolate.\n"
    
#     if any(word in query_lower for word in ["nutrition", "baby", "health"]):
#         context += "**Nutrition**: Gerber baby food, Carnation evaporated milk, focus on nutrition science.\n"
    
#     if any(word in query_lower for word in ["sustainability", "environment"]):
#         context += "**Sustainability**: Committed to sustainable cocoa sourcing, water stewardship, and carbon footprint reduction.\n"
    
#     if any(word in query_lower for word in ["christmas", "holiday", "gift"]):
#         context += "**Holiday Products**: Christmas advent calendars, gift tins, seasonal packaging, perfect for gifting.\n"
    
#     context += "**Company Values**: Good Food, Good Life philosophy, quality ingredients, Canadian manufacturing."
    
#     return context

# def get_emergency_fallback_response(query):
#     """Emergency fallback response if all else fails"""
#     return """Hello! I'm your Nestlé Canada assistant. I'm here to help you with information about our delicious products and services.

# Our popular brands include:
# - **KitKat** - Have a break, have a KitKat
# - **Smarties** - Colorful chocolate treats
# - **Aero** - Light, bubbly chocolate
# - **Coffee-mate** - Coffee creamers and enhancers
# - **Quality Street** - Premium assorted chocolates

# Visit **madewithnestle.ca** to explore our full range of products, recipes, and find where to buy.

# How can I help you with Nestlé products today?"""

# # Serve static files (frontend)
# app.mount("/static", StaticFiles(directory="frontend"), name="static")

# # Serve the main chatbot UI
# @app.get("/")
# def get_chat_ui():
#     """Serve the main chatbot interface"""
#     return FileResponse(os.path.join("frontend", "index.html"))

# # Run the application
# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8000))
#     debug = os.getenv("DEBUG", "False").lower() == "true"
    
#     print(f"🌐 Starting server on port {port}")
#     uvicorn.run(
#         "app:app", 
#         host="0.0.0.0", 
#         port=port, 
#         reload=debug
#     )

# app.py - Main application file for Azure deployment

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn
from dotenv import load_dotenv

# Import your modules from backend folder
from backend.retriever import load_graph, embed_nodes, get_top_nodes
from backend.openai_interface import ask_openai
from backend.web_scraper import scrape_web, get_fallback_nestle_urls

# Load environment variables
load_dotenv()

# ----- Minimal Azure Free-compatible startup logic -----
GRAPH_DIR = "graph"
LOG_DIR = "logs"
GRAPH_FILE = os.path.join(GRAPH_DIR, "graph.pkl")

os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(GRAPH_FILE):
    print("\U0001F4CA graph.pkl not found — building knowledge graph...")
    try:
        from backend.graph_builder import build_graph
        build_graph()
        print("✅ Knowledge graph built successfully.")
    except Exception as e:
        print(f"❌ Error building graph: {e}")
else:
    print("✅ graph.pkl already exists — skipping build.")
# --------------------------------------------------------

app = FastAPI(title="Nestlé AI Chatbot", version="1.0.0")

# Global variables for graph and embeddings
G = None
node_embeddings = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    global G, node_embeddings

    print("🚀 Starting Nestlé AI Chatbot...")

    # Try to load graph and embeddings
    try:
        print("📊 Loading knowledge graph...")
        G = load_graph()
        node_embeddings = embed_nodes(G)
        print(f"✅ Graph loaded successfully with {G.number_of_nodes()} nodes")
    except Exception as e:
        print(f"⚠️ Warning: Could not load graph: {e}")
        G = None
        node_embeddings = None

    print("🎉 Nestlé AI Chatbot is ready!")

# Pydantic model for incoming JSON
class Query(BaseModel):
    question: str

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for Azure App Service"""
    return {
        "status": "healthy",
        "graph_loaded": G is not None,
        "nodes_count": G.number_of_nodes() if G else 0,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Main chat endpoint
@app.post("/chat")
def chat(query: Query):
    """Main chat endpoint that processes user queries"""
    try:
        print(f"[DEBUG] Received query: {query.question}")

        # Get graph context if available
        graph_context = ""
        if G and node_embeddings:
            try:
                top_nodes = get_top_nodes(query.question, G, node_embeddings, k=5)
                graph_context = "\n".join([
                    f"**{node}**: {G.nodes[node]['description']}" 
                    for node in top_nodes if node in G.nodes
                ])
                print(f"[DEBUG] Top graph nodes: {top_nodes}")
            except Exception as e:
                print(f"[DEBUG] Graph retrieval error: {e}")
                graph_context = get_basic_nestle_context(query.question)
        else:
            graph_context = get_basic_nestle_context(query.question)

        # Get web results with improved scraper
        web_results = []
        try:
            web_results = scrape_web(query.question, num_results=5)
            print(f"[DEBUG] Web results found: {len(web_results)}")

            if not web_results:
                web_results = get_fallback_nestle_urls(query.question)
                print(f"[DEBUG] Using fallback URLs: {len(web_results)}")

        except Exception as e:
            print(f"[DEBUG] Web scraping error: {e}")
            web_results = get_fallback_nestle_urls(query.question)

        web_context = "\n".join([f"- {url}" for url in web_results]) if web_results else ""

        full_context = f"""NESTLÉ KNOWLEDGE BASE:
{graph_context}

RELEVANT NESTLÉ WEBSITES:
{web_context}

QUERY CONTEXT: The user is asking about: {query.question}
Please provide a response specifically focused on Nestlé Canada products, services, and information."""

        print(f"[DEBUG] Context length: {len(full_context)}")

        try:
            answer = ask_openai(query.question, full_context)
            print("[DEBUG] AI response generated successfully")
        except Exception as e:
            print(f"[DEBUG] AI response error: {e}")
            answer = get_emergency_fallback_response(query.question)

        return {
            "answer": answer,
            "sources": web_results or []
        }

    except Exception as e:
        print(f"[ERROR] Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_basic_nestle_context(query):
    query_lower = query.lower()

    context = "**Nestlé Canada**: Leading food and beverage company with brands like KitKat, Smarties, Aero, Coffee-mate, and Quality Street.\n"

    if any(word in query_lower for word in ["chocolate", "candy", "sweet"]):
        context += "**Chocolate Brands**: KitKat wafer bars, Smarties colorful chocolates, Aero bubbly chocolate, Quality Street assorted chocolates.\n"

    if any(word in query_lower for word in ["coffee", "beverage", "drink"]):
        context += "**Beverages**: Nespresso premium coffee, Coffee-mate creamers, Carnation hot chocolate.\n"

    if any(word in query_lower for word in ["nutrition", "baby", "health"]):
        context += "**Nutrition**: Gerber baby food, Carnation evaporated milk, focus on nutrition science.\n"

    if any(word in query_lower for word in ["sustainability", "environment"]):
        context += "**Sustainability**: Committed to sustainable cocoa sourcing, water stewardship, and carbon footprint reduction.\n"

    if any(word in query_lower for word in ["christmas", "holiday", "gift"]):
        context += "**Holiday Products**: Christmas advent calendars, gift tins, seasonal packaging, perfect for gifting.\n"

    context += "**Company Values**: Good Food, Good Life philosophy, quality ingredients, Canadian manufacturing."
    return context

def get_emergency_fallback_response(query):
    return """Hello! I'm your Nestlé Canada assistant. I'm here to help you with information about our delicious products and services.

Our popular brands include:
- **KitKat** - Have a break, have a KitKat
- **Smarties** - Colorful chocolate treats
- **Aero** - Light, bubbly chocolate
- **Coffee-mate** - Coffee creamers and enhancers
- **Quality Street** - Premium assorted chocolates

Visit **madewithnestle.ca** to explore our full range of products, recipes, and find where to buy.

How can I help you with Nestlé products today?"""

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main chatbot UI
@app.get("/")
def get_chat_ui():
    return FileResponse(os.path.join("frontend", "index.html"))

# Run the application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    print(f"🌐 Starting server on port {port}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=debug
    )
