# backend/web_scraper.py

import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

def scrape_web(query: str, num_results=5):
    """
    Enhanced web scraper focused on Nestlé-related content
    """
    headers = {
        "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    }
    
    max_results = int(os.getenv("MAX_SEARCH_RESULTS", num_results))
    results = []
    
    print(f"🔍 Starting web search for: '{query}'")
    
    # 1. First try to search specifically on Nestlé websites
    nestle_sites = [
        "madewithnestle.ca",
        "nestle.com", 
        "nestle.ca",
        "corporate.nestle.ca"
    ]
    
    for site in nestle_sites:
        try:
            site_results = search_specific_site(query, site, headers, num_results=2)
            results.extend(site_results)
            if len(results) >= max_results:
                break
            time.sleep(1)  # Be respectful to servers
        except Exception as e:
            print(f"⚠️ Error searching {site}: {e}")
            continue
    
    # 2. If we don't have enough results, do a general Nestlé-focused search
    if len(results) < max_results:
        try:
            general_results = search_nestle_general(query, headers, max_results - len(results))
            results.extend(general_results)
        except Exception as e:
            print(f"⚠️ Error in general search: {e}")
    
    # 3. Remove duplicates and return clean URLs
    seen_urls = set()
    clean_results = []
    for result in results:
        url = extract_clean_url(result)
        if url and url not in seen_urls and is_nestle_related(url):
            seen_urls.add(url)
            clean_results.append(url)
    
    print(f"✅ Found {len(clean_results)} unique Nestlé-related URLs")
    return clean_results[:max_results]

def search_specific_site(query, site, headers, num_results=2):
    """Search within a specific Nestlé site"""
    try:
        # Use DuckDuckGo for site-specific search
        search_query = f"site:{site} {query}"
        encoded_query = quote(search_query)
        search_url = f"https://duckduckgo.com/html/?q={encoded_query}"
        
        print(f"🔍 Searching {site}...")
        
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to search {site}: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Look for DuckDuckGo result links
        for link_elem in soup.find_all('a', class_='result__a'):
            href = link_elem.get('href')
            if href and site in href:
                results.append(href)
                if len(results) >= num_results:
                    break
        
        print(f"✅ Found {len(results)} results from {site}")
        return results
        
    except Exception as e:
        print(f"❌ Error searching {site}: {e}")
        return []

def search_nestle_general(query, headers, num_results=3):
    """General search with Nestlé-specific terms"""
    try:
        # Add Nestlé-specific terms to the query
        enhanced_query = f"Nestlé {query} site:nestle.com OR site:madewithnestle.ca"
        encoded_query = quote(enhanced_query)
        search_url = f"https://duckduckgo.com/html/?q={encoded_query}"
        
        print(f"🔍 Performing general Nestlé search...")
        
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ General search failed: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        for link_elem in soup.find_all('a', class_='result__a'):
            href = link_elem.get('href')
            if href and is_nestle_related(href):
                results.append(href)
                if len(results) >= num_results:
                    break
        
        print(f"✅ Found {len(results)} results from general search")
        return results
        
    except Exception as e:
        print(f"❌ Error in general search: {e}")
        return []

def extract_clean_url(url_string):
    """Extract clean URL from search result"""
    if not url_string:
        return None
    
    try:
        # Handle DuckDuckGo redirect URLs
        if "/l/?uddg=" in url_string:
            import urllib.parse
            clean_url = urllib.parse.unquote(url_string.split("uddg=")[1].split("&")[0])
            return clean_url
        
        # Handle direct URLs
        if url_string.startswith("http"):
            return url_string.split("&")[0]  # Remove tracking parameters
        
        return url_string
    except Exception as e:
        print(f"⚠️ Error cleaning URL {url_string}: {e}")
        return None

def is_nestle_related(url):
    """Check if URL is related to Nestlé"""
    if not url:
        return False
    
    nestle_domains = [
        "nestle.com",
        "nestle.ca", 
        "madewithnestle.ca",
        "corporate.nestle.ca",
        "nestleprofessional.ca",
        "nespresso.com",
        "gerber.com"
    ]
    
    return any(domain in url.lower() for domain in nestle_domains)

def get_fallback_nestle_urls(query):
    """Provide relevant Nestlé URLs based on query content"""
    query_lower = query.lower()
    
    fallback_urls = []
    
    print(f"🔄 Using fallback URLs for query: '{query}'")
    
    if any(word in query_lower for word in ["product", "food", "chocolate", "coffee", "brand"]):
        fallback_urls.extend([
            "https://www.madewithnestle.ca/brands",
            "https://www.nestle.com/brands"
        ])
    
    if any(word in query_lower for word in ["sustainability", "environment", "cocoa", "farming"]):
        fallback_urls.extend([
            "https://www.nestle.com/sustainability",
            "https://www.madewithnestle.ca/sustainability"
        ])
    
    if any(word in query_lower for word in ["recipe", "cooking", "meal", "food"]):
        fallback_urls.append("https://www.madewithnestle.ca/recipes")
    
    if any(word in query_lower for word in ["nutrition", "health", "baby", "infant"]):
        fallback_urls.extend([
            "https://www.nestle.com/nutrition",
            "https://www.gerber.com"
        ])
    
    if any(word in query_lower for word in ["career", "job", "work"]):
        fallback_urls.append("https://www.corporate.nestle.ca/en/careers")
    
    if any(word in query_lower for word in ["christmas", "holiday", "gift"]):
        fallback_urls.extend([
            "https://www.madewithnestle.ca/world-canada",
            "https://www.nestle.com/brands/chocolate-confectionery"
        ])
    
    if any(word in query_lower for word in ["kitkat", "kit kat"]):
        fallback_urls.extend([
            "https://www.madewithnestle.ca/brands/kitkat",
            "https://www.nestle.com/brands/chocolate-confectionery/kit-kat"
        ])
    
    if any(word in query_lower for word in ["smarties"]):
        fallback_urls.extend([
            "https://www.madewithnestle.ca/brands/smarties",
            "https://www.nestle.com/brands/chocolate-confectionery/smarties"
        ])
    
    if any(word in query_lower for word in ["coffee-mate", "coffee mate", "creamer"]):
        fallback_urls.extend([
            "https://www.madewithnestle.ca/brands/coffee-mate",
            "https://www.nestle.com/brands/coffee/coffee-mate"
        ])
    
    # Always include main Nestlé pages if nothing specific found
    if not fallback_urls:
        fallback_urls = [
            "https://www.madewithnestle.ca",
            "https://www.nestle.com",
            "https://www.corporate.nestle.ca"
        ]
    
    # Remove duplicates while preserving order
    unique_urls = []
    seen = set()
    for url in fallback_urls:
        if url not in seen:
            unique_urls.append(url)
            seen.add(url)
    
    print(f"📋 Returning {len(unique_urls)} fallback URLs")
    return unique_urls[:3]

def scrape_specific_url(url, headers=None):
    """Scrape content from a specific URL (for future enhancement)"""
    if not headers:
        headers = {
            "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        }
    
    try:
        print(f"🌐 Scraping content from: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant text content
            content = []
            
            # Get title
            title = soup.find('title')
            if title:
                content.append(f"Title: {title.get_text().strip()}")
            
            # Get main content (adjust selectors based on Nestlé website structure)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                paragraphs = main_content.find_all('p')
                for p in paragraphs[:5]:  # Limit to first 5 paragraphs
                    text = p.get_text().strip()
                    if text and len(text) > 50:  # Only include substantial text
                        content.append(text)
            
            return "\n".join(content)
        else:
            print(f"❌ Failed to scrape {url}: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None