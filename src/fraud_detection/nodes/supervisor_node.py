from src.fraud_detection.tools.risk_calculator_tool import calculate_total_risk
from src.fraud_detection.state.state import AgentState
from langchain_core.messages import AIMessage , SystemMessage , HumanMessage
from src.fraud_detection.LLM.groqLLM import get_groq_llm


llm = get_groq_llm()

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

    total_risk_score = state.get("risk_score", 0)

    
    if total_risk_score <= 30:
        risk_level = "Low"
        investigation_status = "cleared"
    elif total_risk_score <= 60:
        risk_level = "Medium"
        investigation_status = "pending"
    else:
        risk_level = "High" if total_risk_score <= 90 else "Critical"
        investigation_status = "escalated"

    
    summary = f"""⚖️ SUPERVISOR FINAL ASSESSMENT:
        Total Accumulated Risk Score: {total_risk_score}
        Risk Level: {risk_level}
        Decision: {investigation_status.upper()}
        """
    
    
    if investigation_status == "escalated":
        summary += "\n⚠️ ESCALATING TO HUMAN ANALYST - Immediate review required!"
    elif investigation_status == "pending":
        summary += "\n⚠️ FLAGGED FOR MONITORING - Routing to human analyst queue."
    else:  
        summary += "\n✅ Company cleared - Low risk. Closing investigation."

    
    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT),
        HumanMessage(content=summary)
    ]

    response = llm.invoke(messages)
    
    
    return {
        "investigation_status": investigation_status,
        "evidence_log": [response] 
    }
    



