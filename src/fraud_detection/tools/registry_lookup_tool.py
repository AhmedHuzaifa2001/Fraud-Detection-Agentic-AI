from datetime import datetime
from tavily import TavilyClient
from src.fraud_detection.LLM.groqLLM import get_groq_llm
from pydantic import BaseModel , Field
from langchain.messages import SystemMessage , HumanMessage
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class RegistryData(BaseModel):
    exists: bool = Field(description = "True if the search results confirm this is a real company")
    incorporation_date: str = Field(description = "Format YYYY-MM-DD, or Unknown")
    status: str = Field(description = "Active, Dissolved, or Unknown")
    directors:list[str] = Field(description = "Names of key people, or empty list")
    address: str = Field(description = "The physical headquarters, or Address Not Found") 
    jurisdiction: str = Field(description = "The state/country of registration, or Unknown")

MOCK_REGISTRY = {
    "acme corp": {
        "incorporation_date": "2015-03-20",
        "status": "Active",
        "directors": ["Sarah Johnson", "Michael Chen"],
        "address": "123 Business Blvd, Suite 500, New York, NY",
        "jurisdiction": "Delaware"
    },
    "quickcash llc": {
        "incorporation_date": "2026-01-12",  
        "status": "Active",
        "directors": ["John Doe"],  
        "address": "P.O. Box 789, Miami, FL",
        "jurisdiction": "Florida"
    },
    "ghost industries": {
        "incorporation_date": "2020-06-15",
        "status": "Dissolved",
        "directors": ["Unknown"],
        "address": "456 Empty Street, Austin, TX",
        "jurisdiction": "Texas"
    },

    "real business inc": {
        "incorporation_date": "2010-08-10",
        "status": "Active",
        "directors": ["Emma Wilson", "David Martinez", "Lisa Anderson"],
        "address": "789 Corporate Drive, San Francisco, CA",
        "jurisdiction": "California"
},

    "shell corp xyz": {
        "incorporation_date": "2026-01-13",  
        "status": "Active",
        "directors": ["John Doe", "Jane Smith"],  
        "address": "UPS Store #123, Suite 45, Las Vegas, NV",
        "jurisdiction": "Nevada"
}
   
}

def registry_lookup(company_name:str) -> dict:
    
    
    """
    Looks up company registration details from government registry.
    
    Args:
        company_name: Name of the company to lookup
        
    Returns:
        Dictionary with company details or error if not found
    """


    try:
        query = f'"{company_name}" corporate headquarters address, key executives, and company history'

        tavily_response = tavily_client.search(query=query)

        results = tavily_response.get("results", [])
        top_contents = [r.get("content", "") for r in results[:5] if r.get("content")]
        raw_registry_text = "\n\n".join(top_contents)

        llm = get_groq_llm()
        structured_llm = llm.with_structured_output(RegistryData)

        system_prompt = """You are an expert data extractor. Extract company registry and corporate 
        details from the provided search results.
            CRITICAL RULES:
            1. Even if you cannot find official legal registry documents, if the search results 
            clearly indicate that this is a real, operating business or well-known brand, you MUST 
            set 'exists' to True.
            2. If the company operates under a brand name (e.g. 'Optus' instead of 
            'Singtel Optus Pty Ltd'), still treat it as a real company.
            3. If a specific piece of data (like incorporation date or directors) is 
            completely missing, use 'Unknown' or 'Address Not Found', but do not mark the company 
            as fake just because a single field is missing.
            """

        final_message = [
            SystemMessage(content = system_prompt),
            HumanMessage(content = raw_registry_text)
        ]


        response = structured_llm.invoke(final_message)


        company_age_days = None
        if response.incorporation_date and response.incorporation_date.lower() != "unknown":
            try:
                # Assumes the LLM formatted it as YYYY-MM-DD
                inc_date = datetime.strptime(response.incorporation_date, "%Y-%m-%d")
                company_age_days = (datetime.now() - inc_date).days
            except ValueError:
                # If the LLM returns a weird date format, just leave it as None
                pass
        # 2. Return the final dictionary formatted exactly how the rest of the app expects it
        return {
            "exists": response.exists,
            "company_name": company_name,
            "incorporation_date": response.incorporation_date,
            "company_age_days": company_age_days,
            "status": response.status,
            "directors": response.directors,
            "address": response.address,
            "jurisdiction": response.jurisdiction 
        }
    except Exception as e:
        print(f"Registry lookup failed: {e}")
        return {
            "exists": False,
            "company_name": company_name,
            "address": "Address Not Found",
            "error": "Registry search failed due to network or API error."
        }