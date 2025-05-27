# app.py - AZURE FREE TIER COMPATIBLE VERSION
# No startup scripts needed - everything handled in code

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
import uvicorn

# Create app FIRST
app = FastAPI(title="Nestlé AI Chatbot", version="1.0.0")

# Global variables
G = None
node_embeddings = None
components_loaded = False

# ESSENTIAL: Create directories immediately
os.makedirs("graph", exist_ok=True)
os.makedirs("logs", exist_ok=True)
print("📁 Directories created")

class Query(BaseModel):
    question: str

@app.get("/health")
def health_check():
    """Always works - no dependencies"""
    return {
        "status": "healthy",
        "message": "Nestlé Chatbot is running on Azure Free Tier",
        "components_loaded": components_loaded
    }

@app.get("/test")
def simple_test():
    """Ultra simple test endpoint"""
    return {"message": "✅ Nestlé Chatbot API is working!", "azure": "free-tier"}

def load_components_if_needed():
    """Load heavy components only when first needed"""
    global G, node_embeddings, components_loaded
    
    if components_loaded:
        return
    
    print("🔄 Loading components on first request...")
    
    try:
        # Try to load OpenAI
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print("✅ OpenAI configured")
    except Exception as e:
        print(f"⚠️ OpenAI setup issue: {e}")
    
    try:
        # Build minimal graph if needed
        graph_file = os.path.join("graph", "graph.pkl")
        if not os.path.exists(graph_file):
            build_minimal_graph()
    except Exception as e:
        print(f"⚠️ Graph issue: {e}")
    
    components_loaded = True
    print("✅ Components loaded successfully")

def build_minimal_graph():
    """Build graph without heavy dependencies"""
    try:
        import pickle
        
        # Create simple data structure instead of NetworkX
        simple_graph = {
            "KitKat": {
                "description": "Nestlé's iconic chocolate wafer bar. Have a break, have a KitKat!",
                "category": "chocolate"
            },
            "Smarties": {
                "description": "Colorful candy-coated chocolate pieces perfect for sharing and baking.",
                "category": "chocolate"
            },
            "Aero": {
                "description": "Light, bubbly chocolate bars with unique aerated texture.",
                "category": "chocolate"
            },
            "Coffee-mate": {
                "description": "Premium coffee creamers in various delicious flavors.",
                "category": "beverages"
            },
            "Quality Street": {
                "description": "Premium assorted chocolates in colorful wrappers, perfect for gifting.",
                "category": "chocolate"
            },
            "Nestlé Canada": {
                "description": "Leading food and beverage company with beloved Canadian brands.",
                "category": "company"
            }
        }
        
        # Save simple graph
        with open(os.path.join("graph", "graph.pkl"), "wb") as f:
            pickle.dump(simple_graph, f)
        
        print("✅ Minimal graph created")
        return simple_graph
    except Exception as e:
        print(f"❌ Graph creation failed: {e}")
        return {}

def get_simple_context(query):
    """Get context without heavy ML"""
    query_lower = query.lower()
    
    contexts = {
        "kitkat": "**KitKat** is Nestlé's world-famous chocolate wafer bar. With crispy wafer fingers covered in smooth milk chocolate, it's the perfect treat for a break. Available in original, chunky, and seasonal varieties.",
        
        "smarties": "**Smarties** are Nestlé's beloved colorful candy-coated chocolates. Perfect for sharing, parties, baking, and decorating. These bite-sized treats bring joy and color to any occasion.",
        
        "aero": "**Aero** chocolate bars feature Nestlé's unique bubbly texture that melts smoothly in your mouth. The aerated chocolate creates a light, indulgent experience available in milk and dark chocolate.",
        
        "coffee": "**Coffee-mate** offers premium coffee creamers that transform your daily coffee into a delicious experience. Available in classic and seasonal flavors like French Vanilla and Peppermint Mocha.",
        
        "quality street": "**Quality Street** provides an assortment of premium chocolates and toffees in distinctive colorful wrappers. Perfect for sharing during holidays and special celebrations.",
        
        "chocolate": "Nestlé Canada offers an amazing range of **chocolate products** including KitKat wafer bars, Smarties colorful candies, Aero bubbly chocolate, and Quality Street premium assortments.",
        
        "sustainability": "**Nestlé is committed to sustainability** through the Cocoa Plan, supporting farmers, water stewardship, and reducing environmental impact across all operations.",
        
        "nutrition": "Nestlé focuses on **Good Food, Good Life** with products that provide quality ingredients, balanced nutrition, and support for all life stages from infants to seniors."
    }
    
    # Find matching context
    for keyword, context in contexts.items():
        if keyword in query_lower:
            return context
    
    # Default context
    return "**Nestlé Canada** is home to beloved brands like KitKat, Smarties, Aero, Coffee-mate, and Quality Street. We're committed to Good Food, Good Life with quality ingredients and sustainable practices."

def get_smart_response(query):
    """Generate response without OpenAI if needed"""
    query_lower = query.lower()
    
    # Product-specific responses
    if any(word in query_lower for word in ["kitkat", "kit kat"]):
        return """🍫 **KitKat - Have a break, have a KitKat!**

KitKat is Nestlé's iconic chocolate wafer bar that's been bringing joy since 1935. Our crispy wafer fingers are perfectly covered in smooth milk chocolate.

**Available varieties:**
• Original 4-finger bars
• KitKat Chunky for extra indulgence  
• Seasonal flavors and limited editions
• Mini bars perfect for sharing

**Perfect for:** Coffee breaks, sharing with friends, lunchbox treats, or anytime you need a delicious break!

Visit **madewithnestle.ca** to explore our full KitKat range and discover recipes!"""

    elif "smarties" in query_lower:
        return """🌈 **Smarties - Colorful Fun in Every Bite!**

Smarties are Nestlé's beloved candy-coated chocolate pieces that bring color and joy to every occasion.

**Why people love Smarties:**
• Vibrant, colorful candy shells
• Smooth chocolate inside
• Perfect for sharing and parties
• Great for baking and decorating
• Available in various pack sizes

**Fun uses:** Birthday parties, cookie decorating, ice cream toppings, trail mix, and creative baking projects!

Find creative **Smarties recipes** and baking ideas at **madewithnestle.ca**!"""

    elif "aero" in query_lower:
        return """🫧 **Aero - Feel the Bubbles Melt!**

Aero chocolate bars feature Nestlé's unique bubbly texture that creates an incredibly smooth, melt-in-your-mouth experience.

**What makes Aero special:**
• Unique aerated chocolate texture
• Light, bubbly consistency
• Smooth melting experience
• Available in milk and dark chocolate
• Perfect portion sizes

**The Aero experience:** Each bite delivers tiny air bubbles that collapse on your tongue, creating a uniquely satisfying chocolate moment.

Discover more about **Aero** and our chocolate range at **madewithnestle.ca**!"""

    elif any(word in query_lower for word in ["coffee", "coffee-mate"]):
        return """☕ **Coffee-mate - Make Every Cup Special!**

Coffee-mate transforms your daily coffee into a delicious, coffeehouse-quality experience with our premium creamers.

**Popular Coffee-mate flavors:**
• French Vanilla - Classic and smooth
• Hazelnut - Rich and nutty
• Peppermint Mocha - Seasonal favorite
• Original - Perfect coffee complement
• Sugar-free options available

**Perfect for:** Morning coffee, afternoon pick-me-ups, iced coffee creations, and coffee-based desserts.

Explore **Coffee-mate products** and coffee recipes at **madewithnestle.ca**!"""

    elif any(word in query_lower for word in ["sustainability", "environment"]):
        return """🌱 **Nestlé's Commitment to Sustainability**

At Nestlé, we believe in creating a better future through sustainable practices across all our operations.

**Our key sustainability initiatives:**
• **Cocoa Plan**: Supporting sustainable cocoa farming and farmer communities
• **Water Stewardship**: Protecting and preserving water resources
• **Carbon Footprint**: Reducing greenhouse gas emissions across our value chain
• **Sustainable Packaging**: Moving toward recyclable and reusable packaging
• **Responsible Sourcing**: Ensuring ethical supply chain practices

**Our goal:** Creating shared value for communities, environment, and future generations.

Learn more about our **sustainability commitments** at **madewithnestle.ca/sustainability**!"""

    else:
        return """👋 **Welcome to Nestlé Canada!**

I'm here to help you discover our amazing range of products and learn about our commitment to **Good Food, Good Life**.

**🍫 Popular Nestlé Canada brands:**
• **KitKat** - Have a break, have a KitKat!
• **Smarties** - Colorful chocolate treats
• **Aero** - Feel the bubbles melt
• **Coffee-mate** - Make every cup special
• **Quality Street** - Premium chocolates for sharing

**✨ What I can help with:**
• Product information and ingredients
• Recipe ideas and cooking tips
• Sustainability and nutrition facts
• Where to find our products
• Company information and values

**Visit madewithnestle.ca** for recipes, product details, and more!

What would you like to know about Nestlé products?"""

@app.post("/chat")
async def chat(query: Query):
    """Main chat endpoint - works with or without heavy components"""
    try:
        # Load components if this is first request
        load_components_if_needed()
        
        print(f"💬 Query: {query.question}")
        
        # Try OpenAI first if available
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                openai.api_key = api_key
                context = get_simple_context(query.question)
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful Nestlé Canada assistant. Provide friendly, informative responses about Nestlé products, focusing on KitKat, Smarties, Aero, Coffee-mate, and Quality Street. Always mention madewithnestle.ca for more information."},
                        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query.question}"}
                    ],
                    max_tokens=400,
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content.strip()
            else:
                answer = get_smart_response(query.question)
        except Exception as e:
            print(f"OpenAI fallback: {e}")
            answer = get_smart_response(query.question)
        
        # Get relevant URLs
        query_lower = query.question.lower()
        sources = []
        
        if "kitkat" in query_lower:
            sources = ["https://www.madewithnestle.ca/brands/kitkat"]
        elif "smarties" in query_lower:
            sources = ["https://www.madewithnestle.ca/brands/smarties"]
        elif "aero" in query_lower:
            sources = ["https://www.madewithnestle.ca/brands/aero"]
        elif "coffee" in query_lower:
            sources = ["https://www.madewithnestle.ca/brands/coffee-mate"]
        elif "sustainability" in query_lower:
            sources = ["https://www.madewithnestle.ca/sustainability"]
        else:
            sources = [
                "https://www.madewithnestle.ca",
                "https://www.madewithnestle.ca/brands"
            ]
        
        return {
            "answer": answer,
            "sources": sources[:3]
        }
    
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "answer": get_smart_response(query.question),
            "sources": ["https://www.madewithnestle.ca"]
        }

# Serve static files - with fallback
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except Exception as e:
    print(f"Static files warning: {e}")

@app.get("/")
def get_chat_ui():
    """Serve main page with fallback"""
    try:
        html_path = os.path.join("frontend", "index.html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
        else:
            # Fallback HTML if file missing
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Nestlé Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .status { background: #8B4513; color: white; padding: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="status">
        <h1>🏠 Nestlé Chatbot is Running!</h1>
        <p>API is working. Frontend files are loading...</p>
        <p><a href="/test" style="color: white;">Test API</a> | <a href="/health" style="color: white;">Health Check</a></p>
    </div>
</body>
</html>
            """)
    except Exception as e:
        return {"message": "Nestlé Chatbot API is running", "frontend_error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🌐 Starting Nestlé Chatbot on port {port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port)