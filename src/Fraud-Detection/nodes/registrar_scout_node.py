from tools.registry_lookup_tool import registry_lookup
from state.state import AgentState
from tools.risk_calculator_tool import calculate_registry_risk
from langchain_core.messages import HumanMessage

REGISTRAR_SCOUT_PROMPT = """
        You are a Company Registry Investigator specializing in fraud detection.

        Your task: Analyze company registry data and identify suspicious patterns.

        Look for:
        - Newly registered companies (< 7 days old)
        - Dissolved or inactive companies
        - Suspicious director names (John Doe, Unknown, etc.)
        - Missing director information

        Provide a brief analysis summary in 2-3 sentences.
        """

def registrar_scout_node(state:AgentState):

    company_name = state["company_name"]

    data = registry_lookup(company_name)

    risk_score_factors = calculate_registry_risk(data)

    # Format the results into a readable message
    risk_factors_text = "\n- ".join(risk_score_factors["risk_factors"]) if risk_score_factors["risk_factors"] else "No issues found"

    summary = f"""🔍 REGISTRAR SCOUT ANALYSIS:
    Company: {data.get('company_name', 'Unknown')}
    Status: {data.get('status', 'Unknown')}
    Registry Risk Score: {risk_score_factors['risk_score']}

    Red Flags:
    - {risk_factors_text}
    """

    current_score = state.get("risk_score", 0)
    new_score = current_score + risk_score_factors["risk_score"]

    return {
        "registry_data": data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": new_score
    }





