from langchain_core.messages import HumanMessage
from src.fraud_detection.state.state import AgentState

def human_analyst_node(state: AgentState):
    """
    Agent E: Human-in-the-Loop Placeholder.
    This node only triggers if the Supervisor flags the case as Pending or Escalated.
    """
    status = state.get("investigation_status", "unknown").upper()
    
    summary = f"""👨‍💼 HUMAN ANALYST QUEUE:
    This case was marked as {status}. 
    It has been added to the manual review dashboard for a human investigator to approve or reject.
    """
    
    return {
        "evidence_log": [HumanMessage(content=summary)]
    }