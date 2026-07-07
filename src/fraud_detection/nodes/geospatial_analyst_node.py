from src.fraud_detection.tools.geospatial_tool import geospatial_lookup
from src.fraud_detection.state.state import AgentState
from langchain_core.messages import HumanMessage , SystemMessage
from src.fraud_detection.tools.risk_calculator_tool import calculate_geospatial_risk
from src.fraud_detection.LLM.groqLLM import get_groq_llm
from src.fraud_detection.state.state import RegistryAgentRiskAssessment

llm = get_groq_llm()

GEOSPATIAL_ANALYST_PROMPT = """
You are an Address Verification Specialist specializing in fraud detection.
I will provide raw geospatial data. Your task is to evaluate the physical location fraud risk on a scale of 0 to 100.

EVALUATION GUIDELINES:
- Unverified Addresses: Risk score +50 (unless it's a known massive brand).
- P.O. Boxes / Mail Forwarding: Risk score +30 (Often used by shell companies).
- Empty Lots: Risk score +50 (Highly suspicious for operating businesses).
- Zoning Mismatches: Claiming a massive corporate headquarters in a "Residential" zone is a major red flag (+40).

⚠️ CRITICAL EXCEPTIONS:
If the location_type or zoning_type is listed as "Unknown", but the address is explicitly marked as "verified: True", this is a limitation of our mapping tool, NOT a fraud indicator. Do not penalize verified addresses for missing zoning data. 
If no explicit red flags are found, assign a score of 0.

Think step-by-step about the context, list the risk factors, and assign a final calculated score.
"""

def geospatial_analyst_node(state: AgentState):
    """
    Agent B: Geo-Spatial Analyst - Address Verification Specialist.
    
    Analyzes physical address data to identify fake or suspicious locations:
    - Unverified addresses
    - P.O. Boxes and mail forwarding services
    - Empty lots with no structures
    - Zoning mismatches (business in residential area)
    
    Args:
        state: Current agent state containing registry_data with address
        
    Returns:
        Updated state with geo_data, evidence_log, and risk_score
    """
    address = state["registry_data"].get("address" , "Address Unknown")

    if address == "Address Not Found" or address == "Address Unknown":
        address = state.get("company_name" , "Unknown Company")

    geo_data = geospatial_lookup(address)

    risk_score_factors = calculate_geospatial_risk(geo_data)

    
    structure_llm = llm.with_structured_output(RegistryAgentRiskAssessment)


    messages = [
        SystemMessage(content = GEOSPATIAL_ANALYST_PROMPT),
        HumanMessage(content = str(geo_data))
    ]

    assessment = structure_llm.invoke(messages)

    summary = f"""🗺️ GEO-SPATIAL ANALYST REASONING:
    Reasoning: {assessment.reasoning}
    Red Flags: {', '.join(assessment.risk_factors) if assessment.risk_factors else 'None'}
    Assigned Score: {assessment.calculated_score}
    """


    return {
        "geo_data": geo_data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": assessment.calculated_score
    }


