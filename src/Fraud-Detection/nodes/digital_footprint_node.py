from tools.web_search_tool import web_search
from tools.risk_calculator_tool import calculate_digital_risk
from state.state import AgentState
from langchain_core.messages import HumanMessage


DIGITAL_FOOTPRINT_TRACER_PROMPT = """
You are a Digital Footprint Investigator specializing in fraud detection.

Your task: Analyze online presence to detect suspicious digital patterns.

Look for:
- No or minimal online presence (ghost companies)
- Negative keywords (fraud, scam, lawsuit, investigation)
- Missing social media presence
- Weak or non-existent LinkedIn profiles
- Limited professional network connections

Provide a brief analysis summary in 2-3 sentences focusing on digital credibility.
"""

def digital_footprint_node(state: AgentState):
    """
    Agent C: Digital Footprint Tracer - Online Presence Investigator.
    
    Analyzes digital presence to detect suspicious online patterns:
    - No or minimal online presence (ghost companies)
    - Negative keywords (fraud, scam, lawsuit)
    - Missing social media presence
    - Weak or non-existent LinkedIn profiles
    
    Args:
        state: Current agent state containing company_name
        
    Returns:
        Updated state with web_data, evidence_log, and risk_score
    """
    company_name = state["company_name"]

    digital_data = web_search(company_name)

    risk_score_factors = calculate_digital_risk(digital_data)

    risk_factors_text = "\n- ".join(risk_score_factors["risk_factors"]) if risk_score_factors["risk_factors"] else "No issues found"

    negative_keywords = ", ".join(digital_data.get("negative_keywords_found", [])) if digital_data.get("negative_keywords_found") else "None"

    summary = f"""💻 DIGITAL FOOTPRINT TRACER ANALYSIS:
    Company: {company_name}
    Search Results: {digital_data.get('results_count', 0)} found
    Negative Keywords: {negative_keywords}
    Social Media: {'Present' if digital_data.get('social_media_presence', False) else 'Absent'}
    LinkedIn Connections: {digital_data.get('linkedin_connections', 'N/A')}
    Digital Risk Score: {risk_score_factors['risk_score']}

    Red Flags:
    - {risk_factors_text}
    """

    current_score = state.get("risk_score", 0)
    new_score = current_score + risk_score_factors["risk_score"]

    return {
        "web_data": digital_data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": new_score
    }


    