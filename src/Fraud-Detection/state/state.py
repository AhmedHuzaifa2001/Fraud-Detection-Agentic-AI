from typing_extensions import TypedDict , Annotated , Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

StatusOptions = Literal["pending", "escalated", "cleared"]

class AgentState(TypedDict):
    company_name:str
    risk_score:int
    evidence_log : Annotated[list[BaseMessage] , add_messages]

    investigation_status : StatusOptions

    human_analyst_feedback : str | None

