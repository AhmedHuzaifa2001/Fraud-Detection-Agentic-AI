from tools.geospatial_tool import geospatial_lookup
from state.state import AgentState
from langchain_core.messages import HumanMessage
from tools.risk_calculator_tool import calculate_geospatial_risk

GEOSPATIAL_ANALYST_PROMPT = """
You are an Address Verification Specialist specializing in fraud detection.

Your task: Analyze physical address data to identify fake or suspicious business locations.

Look for:
- Unverified addresses that cannot be confirmed
- P.O. Boxes (used to hide real location)
- Mail forwarding services (UPS Store, etc.)
- Empty lots with no physical structure
- Zoning mismatches (e.g., claiming warehouse operation in residential zone)
- Businesses operating from residential addresses inappropriately

Key fraud indicators:
- Shell companies often use P.O. boxes or mail drops
- Legitimate businesses have verifiable physical locations
- Zoning violations suggest false address declarations
- Empty lots indicate completely fabricated addresses

Provide a brief analysis summary in 2-3 sentences focusing on location credibility.
"""

def geospatial_analyst_node(state:AgentState):


    address = state["registry_data"]["address"]

    geo_data = geospatial_lookup(address)

    risk_score_factors = calculate_geospatial_risk(geo_data)

    
    risk_factors_text = "\n- ".join(risk_score_factors["risk_factors"]) if risk_score_factors["risk_factors"] else "No issues found"

    summary = f"""🗺️ GEO-SPATIAL ANALYST ANALYSIS:
    Address: {geo_data.get('address', 'Unknown')}
    Verified: {geo_data.get('verified', False)}
    Location Type: {geo_data.get('location_type', 'Unknown')}
    Zoning: {geo_data.get('zoning_type', 'Unknown')}
    Geospatial Risk Score: {risk_score_factors['risk_score']}

    Red Flags:
    - {risk_factors_text}
    """


    current_score = state.get("risk_score", 0)
    new_score = current_score + risk_score_factors["risk_score"]

    return {
        "geo_data": geo_data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": new_score
    }


