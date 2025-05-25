# backend/graph_builder.py

import networkx as nx
import pickle
import os

def build_graph():
    """Build a comprehensive Nestlé knowledge graph"""
    print("🏗️ Building Nestlé knowledge graph...")
    
    G = nx.Graph()

    # Core Nestlé Information
    G.add_node("Nestlé", description="Nestlé is the world's largest food and beverage company, founded in 1866. Known for 'Good Food, Good Life' philosophy and commitment to nutrition, health, and wellness.")
    
    G.add_node("Nestlé Canada", description="Nestlé Canada operates multiple manufacturing facilities and distributes beloved brands across Canada including KitKat, Smarties, Coffee-mate, and Aero.")

    # Major Product Categories
    G.add_node("Chocolate & Confectionery", description="Nestlé's chocolate and confectionery division includes KitKat, Smarties, Aero, Quality Street, and Butterfinger brands.")
    
    G.add_node("Coffee & Beverages", description="Nestlé coffee and beverage portfolio includes Nespresso, Coffee-mate creamers, and various hot chocolate products.")
    
    G.add_node("Dairy & Nutrition", description="Nestlé dairy and nutrition products include Carnation evaporated milk, Gerber baby food, and various nutritional supplements.")
    
    G.add_node("Culinary Solutions", description="Nestlé culinary products include cooking ingredients, ready-to-eat meals, and food service solutions.")

    # Specific Brands - Chocolate & Confectionery
    G.add_node("KitKat", description="KitKat is Nestlé's iconic wafer chocolate bar. 'Have a break, have a KitKat.' Available in various sizes and flavors including chunky varieties and seasonal editions.")
    
    G.add_node("Smarties", description="Smarties are colorful candy-coated chocolate pieces, perfect for children and adults. Available in various pack sizes and often used in baking and decorating.")
    
    G.add_node("Aero", description="Aero chocolate bars feature light, bubbly chocolate with a unique aerated texture. Available in milk chocolate and dark chocolate varieties.")
    
    G.add_node("Quality Street", description="Quality Street offers premium assorted chocolates in distinctive colorful wrappers, perfect for sharing during holidays and special occasions.")
    
    G.add_node("Butterfinger", description="Butterfinger is a crispy peanut butter chocolate bar with a distinctive golden crunch and rich chocolate coating.")

    # Coffee & Beverage Brands
    G.add_node("Nespresso", description="Nespresso offers premium coffee systems with high-quality coffee capsules for home and office use. Committed to sustainable coffee sourcing.")
    
    G.add_node("Coffee-mate", description="Coffee-mate provides coffee creamers and flavor enhancers in various flavors including seasonal varieties like Peppermint Mocha and Gingerbread.")
    
    G.add_node("Carnation Hot Chocolate", description="Carnation hot chocolate mixes provide rich, creamy hot chocolate experience. Available in various flavors and formats.")

    # Nutrition Brands
    G.add_node("Gerber", description="Gerber specializes in baby food and infant nutrition, providing age-appropriate foods for babies and toddlers with focus on nutrition and development.")
    
    G.add_node("Carnation", description="Carnation evaporated milk is a versatile cooking ingredient used in recipes, coffee, and baking. A Canadian kitchen staple since 1899.")

    # Sustainability & Values
    G.add_node("Sustainability", description="Nestlé is committed to sustainable practices including responsible sourcing, water stewardship, carbon footprint reduction, and supporting farming communities.")
    
    G.add_node("Cocoa Sustainability", description="Nestlé's Cocoa Plan focuses on sustainable cocoa farming, supporting farmers, and ensuring responsible sourcing for chocolate products.")
    
    G.add_node("Nutrition Science", description="Nestlé invests in nutrition science research to improve public health, develop functional foods, and create products for different life stages.")
    
    G.add_node("Good Food Good Life", description="Nestlé's corporate philosophy emphasizing the company's commitment to enhancing lives through good food and beverages.")

    # Seasonal & Special Occasions
    G.add_node("Christmas Products", description="Nestlé offers special Christmas and holiday products including advent calendars, gift tins, seasonal flavors, and holiday-themed packaging.")
    
    G.add_node("Gift Ideas", description="Nestlé products make excellent gifts including chocolate gift boxes, coffee sets, advent calendars, and custom gift baskets.")

    # Recipes & Usage
    G.add_node("Recipes", description="Nestlé provides recipes using their products including baking with chocolate chips, cooking with evaporated milk, and coffee creations.")
    
    G.add_node("Baking", description="Many Nestlé products are popular baking ingredients including chocolate chips, cocoa powder, and evaporated milk for cakes, cookies, and desserts.")

    # Company Information
    G.add_node("Manufacturing", description="Nestlé operates manufacturing facilities across Canada, producing products locally and ensuring freshness and quality for Canadian consumers.")
    
    G.add_node("Innovation", description="Nestlé continuously innovates in food technology, nutrition science, and sustainable packaging to meet evolving consumer needs.")
    
    # Website Information
    G.add_node("Made with Nestlé Website", description="madewithnestle.ca is the official Canadian website featuring products, recipes, sustainability information, and brand stories.")

    # Create relationships between nodes
    edges = [
        # Core company relationships
        ("Nestlé", "Nestlé Canada"),
        ("Nestlé", "Good Food Good Life"),
        ("Nestlé", "Sustainability"),
        ("Nestlé", "Nutrition Science"),
        ("Nestlé", "Innovation"),
        ("Nestlé Canada", "Made with Nestlé Website"),
        
        # Product category relationships
        ("Nestlé Canada", "Chocolate & Confectionery"),
        ("Nestlé Canada", "Coffee & Beverages"),
        ("Nestlé Canada", "Dairy & Nutrition"),
        ("Nestlé Canada", "Culinary Solutions"),
        
        # Brand relationships - Chocolate
        ("Chocolate & Confectionery", "KitKat"),
        ("Chocolate & Confectionery", "Smarties"),
        ("Chocolate & Confectionery", "Aero"),
        ("Chocolate & Confectionery", "Quality Street"),
        ("Chocolate & Confectionery", "Butterfinger"),
        
        # Brand relationships - Coffee & Beverages
        ("Coffee & Beverages", "Nespresso"),
        ("Coffee & Beverages", "Coffee-mate"),
        ("Coffee & Beverages", "Carnation Hot Chocolate"),
        
        # Brand relationships - Nutrition
        ("Dairy & Nutrition", "Gerber"),
        ("Dairy & Nutrition", "Carnation"),
        
        # Sustainability connections
        ("Sustainability", "Cocoa Sustainability"),
        ("Cocoa Sustainability", "KitKat"),
        ("Cocoa Sustainability", "Smarties"),
        ("Cocoa Sustainability", "Aero"),
        ("Cocoa Sustainability", "Quality Street"),
        
        # Special occasions
        ("Christmas Products", "KitKat"),
        ("Christmas Products", "Quality Street"),
        ("Christmas Products", "Smarties"),
        ("Gift Ideas", "Christmas Products"),
        ("Gift Ideas", "Quality Street"),
        ("Gift Ideas", "Coffee-mate"),
        
        # Recipes and usage
        ("Recipes", "Baking"),
        ("Baking", "Smarties"),
        ("Baking", "Carnation"),
        ("Recipes", "Carnation"),
        ("Recipes", "Coffee-mate"),
        ("Made with Nestlé Website", "Recipes"),
        
        # Manufacturing
        ("Manufacturing", "Nestlé Canada"),
        ("Manufacturing", "KitKat"),
        ("Manufacturing", "Smarties"),
        ("Manufacturing", "Aero"),
    ]
    
    G.add_edges_from(edges)

    # Ensure the graph directory exists
    os.makedirs("graph", exist_ok=True)
    
    # Save the graph
    graph_path = os.path.join("graph", "graph.pkl")
    with open(graph_path, "wb") as f:
        pickle.dump(G, f)
    
    print(f"✅ Graph built successfully with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"📁 Graph saved to: {graph_path}")
    
    # Print some sample nodes for verification
    sample_nodes = list(G.nodes())[:5]
    print(f"🔍 Sample nodes: {sample_nodes}")
    
    return G

def add_node_to_graph(node_name, description, connections=None):
    """
    Add a new node to the existing graph
    connections: list of tuples (existing_node, relationship_type)
    """
    try:
        # Load existing graph
        graph_path = os.path.join("graph", "graph.pkl")
        if os.path.exists(graph_path):
            with open(graph_path, "rb") as f:
                G = pickle.load(f)
        else:
            print("⚠️ No existing graph found, creating new one")
            G = nx.Graph()
        
        # Add the new node
        G.add_node(node_name, description=description)
        print(f"➕ Added node: {node_name}")
        
        # Add connections if provided
        if connections:
            for existing_node, relationship in connections:
                if existing_node in G.nodes:
                    G.add_edge(node_name, existing_node)
                    print(f"🔗 Connected {node_name} to {existing_node}")
                else:
                    print(f"⚠️ Node {existing_node} not found in graph")
        
        # Save updated graph
        with open(graph_path, "wb") as f:
            pickle.dump(G, f)
        
        print(f"✅ Graph updated and saved with {G.number_of_nodes()} nodes")
        return True
        
    except Exception as e:
        print(f"❌ Error adding node to graph: {e}")
        return False

def view_graph_info():
    """View information about the current graph"""
    try:
        graph_path = os.path.join("graph", "graph.pkl")
        if not os.path.exists(graph_path):
            print("❌ No graph file found")
            return
        
        with open(graph_path, "rb") as f:
            G = pickle.load(f)
        
        print(f"📊 Graph Information:")
        print(f"   Nodes: {G.number_of_nodes()}")
        print(f"   Edges: {G.number_of_edges()}")
        print(f"   Is Connected: {nx.is_connected(G)}")
        
        print(f"\n🏷️ All Nodes:")
        for i, node in enumerate(sorted(G.nodes()), 1):
            print(f"   {i:2d}. {node}")
        
        print(f"\n🔗 Sample Connections:")
        for i, (node1, node2) in enumerate(list(G.edges())[:10], 1):
            print(f"   {i:2d}. {node1} ↔ {node2}")
        
        if G.number_of_edges() > 10:
            print(f"   ... and {G.number_of_edges() - 10} more connections")
            
    except Exception as e:
        print(f"❌ Error viewing graph info: {e}")

if __name__ == "__main__":
    # Build the graph
    build_graph()
    
    # Show graph information
    print("\n" + "="*50)
    view_graph_info()