# Suspicious director names that indicate fraud
SUSPICIOUS_NAMES = ["john doe", "jane smith", "unknown", "n/a", "not available"]



def calculate_registry_risk(registry_data:dict) -> dict:
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



     

    

