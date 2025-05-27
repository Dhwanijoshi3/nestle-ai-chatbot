# backend/__init__.py
pass

# backend/openai_interface.py
import openai
import os

def ask_openai(question, context=""):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{context}\n{question}"}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except:
        return "I'm here to help with Nestlé products! Visit madewithnestle.ca for more info."

# backend/web_scraper.py  
def get_fallback_nestle_urls(query):
    return ["https://www.madewithnestle.ca"]

def scrape_web(query, num_results=1):
    return get_fallback_nestle_urls(query)

# backend/retriever.py
def load_graph():
    return None

def embed_nodes(graph):
    return None

def get_top_nodes(query, graph, embeddings, k=3):
    return []

# backend/graph_builder.py
def build_graph():
    return None