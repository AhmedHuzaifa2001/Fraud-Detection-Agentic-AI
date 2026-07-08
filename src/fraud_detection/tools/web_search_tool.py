import os
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS 
from tavily import TavilyClient
load_dotenv()


api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key)
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")



SOCIAL_MEDIA_DOMAINS = ["linkedin.com", "twitter.com", "x.com", "facebook.com", 
                        "instagram.com", "youtube.com"]


def search_official_records(company_name: str) -> dict:

    """Uses Google Custom Search to check .gov and financial news."""

    
    query = f'"{company_name}" (fraud OR lawsuit OR investigation)'
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        
        negative_keywords_found = []
        NEGATIVE_KEYWORDS = ["scam", "fraud", "lawsuit", "convicted", "bankrupt", "investigation"]
        
        for item in items:
            combined_text = (item.get("title", "") + " " + item.get("snippet", "")).lower()
            for keyword in NEGATIVE_KEYWORDS:
                if keyword in combined_text and keyword not in negative_keywords_found:
                    negative_keywords_found.append(keyword)

        return {"negative_keywords_found": negative_keywords_found, "records_found": len(items)}
    except Exception as e:
        print(f"Official search failed: {e}")
        return {"negative_keywords_found": [], "records_found": 0}


def _parse_tavily_results(tavily_response: dict) -> dict:
    """
    Parse raw Tavily API response into our standard format.
    Extracts top result titles and social media URLs.
    """
    results = tavily_response.get("results", [])
    
    top_results = []
    social_profiles_found = []  
    
    for result in results:
        title = result.get("title", "")
        url = result.get("url", "").lower()
        
        top_results.append(title)
        
        # Extract social media presence properly
        for domain in SOCIAL_MEDIA_DOMAINS:
            if domain in url:
                # Keep original case for URL, but avoid duplicates
                original_url = result.get("url")
                if original_url not in social_profiles_found:
                    social_profiles_found.append(original_url) 
                break 
            
    return {
        "top_results": top_results,
        "social_profiles": social_profiles_found,
    }


def search_social_with_tavily(company_name: str) -> dict:
    """Actually calls the Tavily API and parses the results."""
   
    try:
        # Search broadly to catch their main pages and social links
        query = f"{company_name} official website and social media"
        
        # Call the Tavily API
        response = tavily_client.search(query=query, search_depth="basic", max_results=10)
        
        # Pass the raw response to your parser
        return _parse_tavily_results(response)
    except Exception as e:
        print(f"⚠️ Tavily search failed: {e}")
        return {"top_results": [], "social_profiles": []}


def digital_footprint_lookup(company_name: str) -> dict:
    """The master function that your LangGraph Node will call."""
    
   
    official_data = search_official_records(company_name)
    social_data = search_social_with_tavily(company_name)
    
    return {
        "search_successful": True,
        "negative_keywords_found": official_data["negative_keywords_found"],
        "official_records_count": official_data["records_found"],
        "social_profiles": social_data
    }