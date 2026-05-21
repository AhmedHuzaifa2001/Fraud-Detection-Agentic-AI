from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=api_key)

# Negative keywords for fraud detection
NEGATIVE_KEYWORDS = ["scam", "fraud", "lawsuit", "convicted", "bankrupt", 
                     "investigation", "illegal"]
# Social media domains to check for presence
SOCIAL_MEDIA_DOMAINS = ["linkedin.com", "twitter.com", "x.com", "facebook.com", 
                        "instagram.com", "youtube.com"]

def _parse_tavily_results(query: str, tavily_response: dict) -> dict:
    """
    Parse raw Tavily API response into our standard format.
    
    Extracts:
    - Top result titles
    - Negative keyword detection from titles and content
    - Social media presence from result URLs
    - LinkedIn connection info (if LinkedIn result found)
    """
    results = tavily_response.get("results", [])
    results_count = len(results)

    # Extract top result titles
    top_results = [r.get("title", "") for r in results[:5]]

    # Scan for negative keywords in titles and content
    negative_keywords_found = []
    for result in results:
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        combined_text = title + " " + content
        for keyword in NEGATIVE_KEYWORDS:
            if keyword in combined_text and keyword not in negative_keywords_found:
                negative_keywords_found.append(keyword)

    # Check for social media presence in result URLs
    social_media_presence = False
    linkedin_connections = None
    for result in results:
        url = result.get("url", "").lower()
        for domain in SOCIAL_MEDIA_DOMAINS:
            if domain in url:
                social_media_presence = True
                break

        # Check specifically for LinkedIn
        if "linkedin.com" in url:
            linkedin_connections = url

    return {
        "query": query,
        "results_count": results_count,
        "top_results": top_results,
        "negative_keywords_found": negative_keywords_found,
        "social_media_presence": social_media_presence,
        "linkedin_connections": linkedin_connections,
        "search_successful": True
    }


def web_search(query: str) -> dict:
    """
    Search the web for a company or person to detect digital footprint.
    
    Uses Tavily API for real web search. Falls back to mock data
    if the API call fails (network error, rate limit, etc.).
    
    Args:
        query: Company name or person name to search
        
    Returns:
        Dictionary with search results including presence indicators
    """
    print(f"Searching the web for: {query}")
    # real Tavily search first
    try:
        tavily_response = tavily_client.search(
            query=f"{query} company information",
            max_results=10,
            search_depth="basic"
        )
        
        parsed = _parse_tavily_results(query, tavily_response)
        print(f"✅ Tavily search successful - {parsed['results_count']} results found")
        return parsed
    
    except Exception as e:
        print(f"⚠️ Tavily search failed: {e}. Falling back to mock data.")
        return _mock_search_fallback(query)
    

def _mock_search_fallback(query: str) -> dict:
    """
    Fallback to mock data when Tavily API is unavailable.
    Returns mock results for known test companies, or empty results for unknown queries.
    """
    normalized_query = query.lower().strip()
    # Check mock company data
    if normalized_query in MOCK_COMPANY_SEARCHES:
        company_data = MOCK_COMPANY_SEARCHES[normalized_query]
        return {
            "query": query,
            "results_count": company_data["results_count"],
            "top_results": company_data["top_results"],
            "negative_keywords_found": company_data["negative_keywords_found"],
            "social_media_presence": company_data["social_media_presence"],
            "linkedin_connections": company_data["linkedin_connections"],
            "search_successful": True
        }
    # Check mock person data
    if normalized_query in MOCK_PERSON_SEARCHES:
        person_data = MOCK_PERSON_SEARCHES[normalized_query]
        return {
            "query": query,
            "results_count": person_data["results_count"],
            "top_results": person_data["top_results"],
            "negative_keywords_found": person_data["negative_keywords_found"],
            "social_media_presence": person_data["social_media_presence"],
            "linkedin_connections": person_data["linkedin_connections"],
            "search_successful": True
        }
    # Unknown query
    return {
        "query": query,
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": None,
        "search_successful": False
    }
# ============================================================
# Mock Data (kept as fallback)
# ============================================================


MOCK_COMPANY_SEARCHES = {
    "acme corp": {
        "results_count": 850,
        "top_results": [
            "Acme Corp - Leading Manufacturing Company",
            "Acme Corp Annual Report 2025",
            "Acme Corp Wins Industry Award",
            "Acme Corp Official Website - About Us"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": None
    },
    "quickcash llc": {
        "results_count": 3,
        "top_results": [
            "QuickCash LLC - Business Registration",
            "QuickCash LLC Contact Information"
        ],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": None
    },
    "ghost industries": {
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": None
    },
    "real business inc": {
        "results_count": 450,
        "top_results": [
            "Real Business Inc - Corporate Profile",
            "Real Business Inc Leadership Team",
            "Real Business Inc Press Releases",
            "Real Business Inc Customer Reviews"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": None
    },
    "shell corp xyz": {
        "results_count": 12,
        "top_results": [
            "Local News: Shell Corp XYZ Under Investigation",
            "Shell Corp XYZ Lawsuit Filed by Investors",
            "Shell Corp XYZ Business Registration"
        ],
        "negative_keywords_found": ["lawsuit", "investigation"],
        "social_media_presence": False,
        "linkedin_connections": None
    }
}
MOCK_PERSON_SEARCHES = {
    "sarah johnson": {
        "results_count": 340,
        "top_results": [
            "Sarah Johnson - CEO Profile LinkedIn",
            "Sarah Johnson Speaking at Tech Conference 2025",
            "Interview with Sarah Johnson - Business Today",
            "Sarah Johnson Awards and Recognition"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": 520
    },
    "john doe": {
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": 0
    },
    "unknown": {
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": 0
    },
    "emma wilson": {
        "results_count": 180,
        "top_results": [
            "Emma Wilson - LinkedIn Profile",
            "Emma Wilson Professional Background",
            "Emma Wilson Board Member Profile"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": 310
    },
    "michael chen": {
        "results_count": 220,
        "top_results": [
            "Michael Chen - Executive Profile",
            "Michael Chen LinkedIn",
            "Michael Chen Industry Experience"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": 425
    },
    "david martinez": {
        "results_count": 165,
        "top_results": [
            "David Martinez - Professional Profile",
            "David Martinez Business Network",
            "David Martinez LinkedIn"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": 280
    },
    "lisa anderson": {
        "results_count": 195,
        "top_results": [
            "Lisa Anderson - Corporate Executive",
            "Lisa Anderson LinkedIn Profile",
            "Lisa Anderson Professional Bio"
        ],
        "negative_keywords_found": [],
        "social_media_presence": True,
        "linkedin_connections": 350
    },
    "jane smith": {
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": 0
    }
}
