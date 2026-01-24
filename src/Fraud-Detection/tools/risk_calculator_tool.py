# Suspicious director names that indicate fraud
SUSPICIOUS_NAMES = ["john doe", "jane smith", "unknown", "n/a", "not available"]



def calculate_registry_risk(registry_data:dict) -> dict:
    """
    Calculate risk score based on company registry data.
    
    Checks for:
    - Company existence in registry
    - Company age (newly registered companies)
    - Company status (dissolved/inactive)
    - Suspicious or missing director names
    """
    risk_score = 0
    risk_factors = []

    if registry_data.get('exists') == False:
        risk_score += 100
        risk_factors.append("Company not found in registry")
        return {"risk_score": risk_score, "risk_factors": risk_factors}
    
  
    company_age_days = registry_data.get("company_age_days")
    if company_age_days and company_age_days < 7:
        risk_score += 20
        risk_factors.append(f"Company is only {company_age_days} days old")
        

    status = registry_data.get('status', "").lower().strip()

    if status == 'inactive' or status == 'dissolved':
        risk_score += 100
        risk_factors.append(f"Company status: {status}")

    directors = registry_data.get('directors')

    if not directors:
        risk_score += 15
        risk_factors.append("No directors listed")
    else:
        for name in directors:
            if name.lower() in SUSPICIOUS_NAMES:
                risk_score += 10
                risk_factors.append(f"Suspicious director name: {name}")

    return {"risk_score": risk_score, "risk_factors": risk_factors}


def calculate_geospatial_risk(geo_data: dict) -> dict:
    """
    Calculate risk score based on geospatial data.
    
    Checks for:
    - Unverified addresses
    - P.O. Boxes and mail forwarding services
    - Empty lots
    - Zoning mismatches (e.g., business in residential area)
    """
    risk_score = 0
    risk_factors = []

    if not geo_data.get("verified", False):
        risk_score += 50
        risk_factors.append("Address could not be verified")

    if geo_data.get("is_po_box", False):
        risk_score += 30
        risk_factors.append("Address is a P.O. Box")

    if geo_data.get("is_ups_store", False):
        risk_score += 30
        risk_factors.append("Address is a mail forwarding service")

    if geo_data.get("location_type") == "Empty Lot":
        risk_score += 50
        risk_factors.append("Address is an empty lot")

    if geo_data.get("zoning_type") == "Residential" and geo_data.get("location_type") != "House":
        risk_score += 40
        risk_factors.append("Business operating from residential address")

    return {"risk_score": risk_score, "risk_factors": risk_factors}


def calculate_digital_risk(web_data: dict) -> dict:
    """
    Calculate risk score based on digital footprint data.
    
    Checks for:
    - Online presence and search results
    - Negative keywords (fraud, scam, lawsuit, etc.)
    - Social media presence
    - LinkedIn profile and network size
    """
    risk_score = 0
    risk_factors = []

    results_count = web_data.get("results_count", 0)
    if results_count == 0:
        risk_score += 25
        risk_factors.append("No online presence found")

    negative_keywords_found = web_data.get("negative_keywords_found", [])
    if negative_keywords_found:
        risk_score += 40
        keywords = ", ".join(negative_keywords_found)
        risk_factors.append(f"Negative keywords found: {keywords}")

    social_media_presence = web_data.get("social_media_presence", False)
    if not social_media_presence:
        risk_score += 15
        risk_factors.append("No social media presence")

    linkedin_connections = web_data.get("linkedin_connections", 0)
    if linkedin_connections == 0:
        risk_score += 15
        risk_factors.append("No LinkedIn profile found")
    elif linkedin_connections < 50:
        risk_score += 10
        risk_factors.append(f"Limited LinkedIn network ({linkedin_connections} connections)")

    return {"risk_score": risk_score, "risk_factors": risk_factors}


def calculate_total_risk(registry_data: dict, geo_data: dict, web_data: dict) -> dict:
    """
    Calculate total fraud risk score by combining all data sources.
    
    Calls all three specialized risk calculators and combines their results
    into a comprehensive risk assessment with categorized risk level.
    
    Risk Levels:
    - Low: 0-30 points
    - Medium: 31-60 points
    - High: 61-90 points
    - Critical: 91+ points
    """
    # Calculate individual risk scores
    registry_result = calculate_registry_risk(registry_data)
    geo_result = calculate_geospatial_risk(geo_data)
    digital_result = calculate_digital_risk(web_data)
    
    # Combine scores
    total_score = (
        registry_result["risk_score"] +
        geo_result["risk_score"] +
        digital_result["risk_score"]
    )
    
    # Combine all risk factors
    all_risk_factors = (
        registry_result["risk_factors"] +
        geo_result["risk_factors"] +
        digital_result["risk_factors"]
    )
    
    # Determine risk level
    if total_score <= 30:
        risk_level = "Low"
    elif total_score <= 60:
        risk_level = "Medium"
    elif total_score <= 90:
        risk_level = "High"
    else:
        risk_level = "Critical"
    
    return {
        "total_risk_score": total_score,
        "risk_level": risk_level,
        "risk_factors": all_risk_factors,
        "breakdown": {
            "registry_score": registry_result["risk_score"],
            "geospatial_score": geo_result["risk_score"],
            "digital_score": digital_result["risk_score"]
        }
    }
