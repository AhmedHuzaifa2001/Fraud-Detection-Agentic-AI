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