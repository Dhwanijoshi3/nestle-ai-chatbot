# backend/retriever.py

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Initialize the sentence transformer model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Sentence transformer model loaded successfully")
except Exception as e:
    print(f"❌ Error loading sentence transformer: {e}")
    model = None

def load_graph():
    """Load the knowledge graph from pickle file"""
    graph_path = os.path.join("graph", "graph.pkl")
    
    if not os.path.exists(graph_path):
        print(f"❌ Graph file not found at {graph_path}")
        raise FileNotFoundError(f"Graph file not found at {graph_path}")
    
    try:
        with open(graph_path, "rb") as f:
            graph = pickle.load(f)
        print(f"✅ Graph loaded with {graph.number_of_nodes()} nodes")
        return graph
    except Exception as e:
        print(f"❌ Error loading graph: {e}")
        raise e

def embed_nodes(G):
    """Create embeddings for all nodes in the graph"""
    if not model:
        print("❌ Sentence transformer model not available")
        return {}
    
    try:
        embeddings = {}
        print("📊 Creating node embeddings...")
        
        for node in G.nodes:
            desc = G.nodes[node].get('description', '')
            if desc:
                embeddings[node] = model.encode(desc)
            else:
                # Use node name if no description
                embeddings[node] = model.encode(str(node))
        
        print(f"✅ Created embeddings for {len(embeddings)} nodes")
        return embeddings
    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        return {}

def get_top_nodes(query, G, node_embeddings, k=3):
    """Get the top k most relevant nodes for a given query"""
    if not model or not node_embeddings:
        print("❌ Model or embeddings not available")
        return []
    
    try:
        # Encode the query
        query_emb = model.encode(query)
        
        # Calculate similarities
        similarities = {}
        for node, emb in node_embeddings.items():
            if node in G.nodes:  # Ensure node still exists in graph
                similarity = np.dot(query_emb, emb) / (
                    np.linalg.norm(query_emb) * np.linalg.norm(emb)
                )
                similarities[node] = similarity
        
        # Sort by similarity and return top k
        top_nodes = sorted(similarities.keys(), key=lambda x: similarities[x], reverse=True)[:k]
        
        print(f"🔍 Found {len(top_nodes)} relevant nodes for query: '{query}'")
        return top_nodes
    
    except Exception as e:
        print(f"❌ Error finding relevant nodes: {e}")
        return []

def get_node_context(node, G, max_description_length=200):
    """Get formatted context for a specific node"""
    if node not in G.nodes:
        return ""
    
    description = G.nodes[node].get('description', str(node))
    
    # Truncate if too long
    if len(description) > max_description_length:
        description = description[:max_description_length] + "..."
    
    return description

def get_connected_nodes(node, G, depth=1):
    """Get nodes connected to the given node up to specified depth"""
    if node not in G.nodes:
        return []
    
    connected = set()
    current_level = {node}
    
    for _ in range(depth):
        next_level = set()
        for current_node in current_level:
            neighbors = set(G.neighbors(current_node))
            next_level.update(neighbors)
            connected.update(neighbors)
        current_level = next_level
    
    return list(connected)

def search_graph_content(query, G, node_embeddings, max_results=5, include_connected=True):
    """
    Comprehensive search of graph content
    """
    if not G or not node_embeddings:
        return ""
    
    try:
        # Get top relevant nodes
        top_nodes = get_top_nodes(query, G, node_embeddings, k=max_results)
        
        context_parts = []
        processed_nodes = set()
        
        for node in top_nodes:
            if node in processed_nodes:
                continue
                
            # Add main node context
            description = get_node_context(node, G)
            context_parts.append(f"**{node}**: {description}")
            processed_nodes.add(node)
            
            # Optionally include connected nodes for richer context
            if include_connected:
                connected = get_connected_nodes(node, G, depth=1)
                for connected_node in connected[:2]:  # Limit to avoid too much text
                    if connected_node not in processed_nodes:
                        connected_desc = get_node_context(connected_node, G, max_description_length=100)
                        context_parts.append(f"*Related - {connected_node}*: {connected_desc}")
                        processed_nodes.add(connected_node)
        
        return "\n".join(context_parts)
    
    except Exception as e:
        print(f"❌ Error searching graph content: {e}")
        return ""