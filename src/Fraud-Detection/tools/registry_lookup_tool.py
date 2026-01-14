from datetime import datetime


MOCK_REGISTRY = {
    "acme corp": {
        "incorporation_date": "2015-03-20",
        "status": "Active",
        "directors": ["Sarah Johnson", "Michael Chen"],
        "address": "123 Business Blvd, Suite 500, New York, NY",
        "jurisdiction": "Delaware"
    },
    "quickcash llc": {
        "incorporation_date": "2026-01-12",  # 2 days ago!
        "status": "Active",
        "directors": ["John Doe"],  # Suspicious generic name
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
        "incorporation_date": "2026-01-13",  # 1 day old!
        "status": "Active",
        "directors": ["John Doe", "Jane Smith"],  # Generic names
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

    print(f"Checking the {company_name} database")


    normalized_company_name = company_name.lower().strip()

     ## checking if company exists

    company_data = MOCK_REGISTRY.get(normalized_company_name)

    if company_data:

        incorporation_date_str = company_data["incorporation_date"]
        try:
            incorporation_date = datetime.strptime(incorporation_date_str, "%Y-%m-%d")
            company_age_days = (datetime.now() - incorporation_date).days
        except ValueError:
            company_age_days = None

        return{
               "exists" : True,
               "company_name" : company_name,
               "incorporation_date" : company_data["incorporation_date"],
               "company_age_days": company_age_days,
               "status" : company_data["status"],
               "directors": company_data["directors"],
               "address":company_data["address"],
               "jurisdiction" : company_data["jurisdiction"] 
          }
     
    else:
         return{
             
               "exists" : False,
               "company_name" : company_name,
                "error": "Company not found in registry"
         } 

    
