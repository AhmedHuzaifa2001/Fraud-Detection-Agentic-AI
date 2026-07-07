from typing_extensions import TypedDict , Annotated , Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import operator
from pydantic import BaseModel , Field
StatusOptions = Literal["pending", "escalated", "cleared"]


class RegistryAgentRiskAssessment(BaseModel):
    reasoning: str = Field(description="A step-by-step explanation of why this data is or isn't suspicious.")
    risk_factors: list[str] = Field(description="A list of specific red flags found, or an empty list if none.")
    calculated_score: int = Field(description="An assigned risk score from 0 to 100 based on the evidence.")



class AgentState(TypedDict):
    company_name: str
    risk_score: Annotated[int , operator.add]
    evidence_log: Annotated[list[BaseMessage], add_messages]
    investigation_status: StatusOptions
    human_analyst_feedback: str | None
    registry_data: dict | None
    geo_data: dict | None
    web_data: dict | None

