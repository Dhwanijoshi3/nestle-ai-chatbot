# backend/openai_interface.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if using Azure OpenAI (optional for future)
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if azure_endpoint:
    openai.api_type = "azure"
    openai.api_base = azure_endpoint
    openai.api_version = "2023-12-01-preview"

def ask_openai(question: str, context: str = "") -> str:
    """
    Ask OpenAI a question with optional context
    """
    try:
        # Prepare the system message
        system_message = """You are a helpful AI assistant for Nestlé Canada. You provide accurate information about Nestlé products, services, sustainability practices, and company information.

Key guidelines:
- Always be friendly and professional
- Focus on Nestlé Canada products and services
- Provide specific product information when possible
- Include sustainability and nutrition information when relevant
- If you don't have specific information, acknowledge it and provide general Nestlé information
- Always try to be helpful and direct users to madewithnestle.ca for more information
- Use proper formatting with headings and bullet points for readability

Popular Nestlé Canada brands include:
- KitKat (chocolate wafer bars)
- Smarties (colorful chocolate candies)
- Aero (bubbly chocolate bars)
- Quality Street (assorted chocolates)
- Coffee-mate (coffee creamers)
- Carnation (evaporated milk, hot chocolate)
- Butterfinger (crispy peanut butter bars)"""

        # Prepare the user message
        user_message = f"""Question: {question}

Context Information:
{context}

Please provide a helpful response about Nestlé Canada products, services, or information related to this question."""

        # Make the API call
        if azure_endpoint:
            # Azure OpenAI
            response = openai.ChatCompletion.create(
                engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
        else:
            # Standard OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"[ERROR] OpenAI API error: {e}")
        return get_fallback_response(question)

def get_fallback_response(question: str) -> str:
    """
    Provide a fallback response when OpenAI is not available
    """
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["kitkat", "kit kat", "chocolate", "wafer"]):
        return """**KitKat** is one of Nestlé's most beloved chocolate brands! 

KitKat features crispy wafer fingers covered in smooth milk chocolate. The iconic slogan "Have a break, have a KitKat" has made it a favorite treat for over 80 years.

**Popular KitKat varieties in Canada:**
- Original 4-finger bars
- KitKat Chunky varieties
- Seasonal flavors and limited editions
- Mini KitKat bars perfect for sharing

Visit **madewithnestle.ca** to explore our full KitKat range and find delicious recipes using KitKat!"""
    
    elif any(word in question_lower for word in ["smarties", "colorful", "candy"]):
        return """**Smarties** are Nestlé's colorful chocolate candies that bring joy to every occasion!

These bite-sized pieces of chocolate covered in a crispy, colorful shell are perfect for sharing, baking, or enjoying as a sweet treat.

**Fun with Smarties:**
- Available in multiple pack sizes
- Perfect for decorating cakes and cookies
- Great for party favors and celebrations
- Made with sustainably sourced cocoa

Visit **madewithnestle.ca** for creative Smarties recipes and baking ideas!"""
    
    elif any(word in question_lower for word in ["coffee", "coffee-mate", "creamer"]):
        return """**Coffee-mate** makes every cup of coffee special with our delicious creamers!

Coffee-mate offers a variety of flavors to enhance your coffee experience, from classic French Vanilla to seasonal favorites like Peppermint Mocha.

**Coffee-mate Products:**
- Liquid creamers in various flavors
- Powdered creamers for convenience
- Seasonal and limited edition flavors
- Sugar-free options available

Transform your daily coffee routine with Coffee-mate! Visit **madewithnestle.ca** for more information."""
    
    elif any(word in question_lower for word in ["sustainability", "environment", "cocoa"]):
        return """**Nestlé is committed to sustainability** across all our operations and products.

**Our Sustainability Commitments:**
- **Cocoa Plan**: Supporting sustainable cocoa farming and farmer communities
- **Water Stewardship**: Protecting water resources in our operations and communities  
- **Carbon Footprint**: Reducing greenhouse gas emissions across our value chain
- **Sustainable Packaging**: Working toward recyclable and reusable packaging

Learn more about our sustainability initiatives at **madewithnestle.ca/sustainability**."""
    
    else:
        return """Hello! I'm your Nestlé Canada assistant. I'm here to help you with information about our delicious products and services.

**Popular Nestlé Canada Brands:**
- **KitKat** - Have a break, have a KitKat
- **Smarties** - Colorful chocolate treats  
- **Aero** - Light, bubbly chocolate
- **Coffee-mate** - Coffee creamers and enhancers
- **Quality Street** - Premium assorted chocolates
- **Carnation** - Evaporated milk and hot chocolate

Visit **madewithnestle.ca** to explore our full range of products, recipes, and learn about our commitment to Good Food, Good Life.

How can I help you with Nestlé products today?"""