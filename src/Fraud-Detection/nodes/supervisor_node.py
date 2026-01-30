from tools.risk_calculator_tool import calculate_total_risk
from state.state import AgentState
from langchain_core.messages import AIMessage


SUPERVISOR_PROMPT = """
You are the Investigation Supervisor coordinating fraud detection.

Your role: Review all evidence and make final decisions.

Available evidence:
- Registry analysis (company legal status)
- Geospatial analysis (address verification)
- Digital footprint analysis (online presence)

Decision criteria:
- Low Risk (0-30): Clear the company
- Medium Risk (31-60): Clear but flag for monitoring
- High Risk (61-90): Escalate to human analyst
- Critical Risk (91+): Escalate to human analyst immediately
"""


def supervisor_node(state: AgentState):
    """
    Agent D: Supervisor - Investigation coordinator and decision maker.
    
    Reviews all evidence from detection agents and makes final risk assessment.
    Calls calculate_total_risk() to combine all findings.
    Updates investigation_status based on risk level.
    """

    ## Get all data

    registry_data = state["registry_data"]
    geo_data = state["geo_data"]
    web_data = state["web_data"]

    final_assessment = calculate_total_risk(registry_data , geo_data , web_data)

    total_risk_score = final_assessment["total_risk_score"]
    risk_level = final_assessment["risk_level"]
    breakdown = final_assessment["breakdown"]

    if risk_level == "Critical" or risk_level == "High":
        investigation_status = "escalated"

    elif risk_level == "Medium":
        investigation_status = "pending"

    else:  # Low
        investigation_status = "cleared"


    summary = f"""⚖️ SUPERVISOR FINAL ASSESSMENT:
        Total Risk Score: {total_risk_score}
        Risk Level: {risk_level}
        Decision: {investigation_status.upper()}

        Score Breakdown:
        - Registry: {breakdown['registry_score']}
        - Geospatial: {breakdown['geospatial_score']}
        - Digital: {breakdown['digital_score']}

        """

    
    if investigation_status == "escalated":
        summary += "⚠️ ESCALATING TO HUMAN ANALYST - Immediate review required!"
    elif investigation_status == "pending":
        summary += "⚠️ FLAGGED FOR MONITORING - Medium risk detected"
    else:  
        summary += "✅ Company cleared - Low risk"


    return{
        "risk_score": total_risk_score,
        "investigation_status": investigation_status,
        "evidence_log": [AIMessage(content=summary)] # AIMessage (supervisor's decision)
    }
    

# HumanMessage = "Here's data" (observation)
# AIMessage = "Here's my decision" (reasoning)
# The supervisor is the only one making a decision, the others just report findings
# that is why we used AIMessage to this Node and other Nodes with HumanMessage




