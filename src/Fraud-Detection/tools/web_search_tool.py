from tavily import TavilyClient

# Negative keywords for fraud detection
NEGATIVE_KEYWORDS = ["scam", "fraud", "lawsuit", "convicted", "bankrupt", "investigation", "illegal"]

# Mock company search results
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

# Mock person/director search results
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


def web_search(query:str) -> dict:
    """
    Simulates web search for company or person to detect digital footprint.
    
    In production, this would use Tavily API or similar web search service.
    
    Args:
        query: Company name or person name to search
        
    Returns:
        Dictionary with search results including presence indicators
    """
    print(f"Searching the web for the: {query}")

    normalized_query = query.lower().strip()



    if normalized_query in MOCK_COMPANY_SEARCHES:
        company_data = MOCK_COMPANY_SEARCHES.get(normalized_query)

        
        return {
                "query": query,  # Use original, not normalized
                "results_count": company_data["results_count"],
                "top_results": company_data["top_results"],
                "negative_keywords_found": company_data["negative_keywords_found"],
                "social_media_presence": company_data["social_media_presence"],
                "linkedin_connections": company_data["linkedin_connections"],
                "search_successful": True
            }
    
    if normalized_query in MOCK_PERSON_SEARCHES:
        person_data = MOCK_PERSON_SEARCHES.get(normalized_query)

        
        return {
                "query": query,
                "results_count": person_data["results_count"],
                "top_results": person_data["top_results"],
                "negative_keywords_found": person_data["negative_keywords_found"],
                "social_media_presence": person_data["social_media_presence"],
                "linkedin_connections": person_data["linkedin_connections"],
                "search_successful": True
            }

    else:
         return {
        "query": query,
        "results_count": 0,
        "top_results": [],
        "negative_keywords_found": [],
        "social_media_presence": False,
        "linkedin_connections": None,
        "search_successful": True
    }




