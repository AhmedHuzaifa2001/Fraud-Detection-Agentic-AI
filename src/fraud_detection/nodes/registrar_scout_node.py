from src.fraud_detection.tools.registry_lookup_tool import registry_lookup
from src.fraud_detection.state.state import AgentState
from src.fraud_detection.LLM.groqLLM import get_groq_llm
from src.fraud_detection.tools.risk_calculator_tool import calculate_registry_risk
from langchain_core.messages import HumanMessage , SystemMessage
from pydantic import BaseModel , Field


class RegistryAgentRiskAssessment(BaseModel):
    reasoning: str = Field(description="A step-by-step explanation of why this data is or isn't suspicious.")
    risk_factors: list[str] = Field(description="A list of specific red flags found, or an empty list if none.")
    calculated_score: int = Field(description="An assigned risk score from 0 to 100 based on the evidence.")


llm = get_groq_llm()

REGISTRAR_SCOUT_PROMPT = """
You are a Company Registry Investigator specializing in fraud detection. 
I will provide raw registry data. Your task is to evaluate the fraud risk on a scale of 0 to 100.

EVALUATION GUIDELINES:
- Age: Brand new companies (< 7 days) are slightly risky.
- Status: Dissolved or inactive companies actively conducting business are massive red flags (Score > 80).
- Directors: Generic names (John Doe) or completely missing directors warrant higher risk scores.

⚠️ CRITICAL EXCEPTIONS FOR WELL-KNOWN BRANDS:
If the company is a globally recognized, massive corporation (e.g., Google, Microsoft, Apple, Amazon), and fields like 'directors' or 'incorporation_date' are missing or empty, you MUST assume this is a limitation of our web search tool, NOT an indicator of fraud. 
Do not penalize famous mega-corporations for missing generic registry fields. Assign them a very low risk score (0-10) unless their status is explicitly 'Dissolved'.

Think step-by-step about the context, list the risk factors, and assign a final calculated score.
"""



def registrar_scout_node(state: AgentState):
    """
    Agent A: Registrar Scout - Company Registry Investigator.
    
    Analyzes company registry data to detect fraud patterns including:
    - Company existence verification
    - New company registrations (< 7 days)
    - Dissolved or inactive companies
    - Suspicious or missing director information
    
    Args:
        state: Current agent state containing company_name
        
    Returns:
        Updated state with registry_data, evidence_log, and risk_score
    """
    company_name = state["company_name"]

    data = registry_lookup(company_name)

    # risk_score_factors = calculate_registry_risk(data)

    structured_llm = llm.with_structured_output(RegistryAgentRiskAssessment)
    # Format the results into a readable message
    # risk_factors_text = "\n- ".join(risk_score_factors["risk_factors"]) if risk_score_factors["risk_factors"] else "No issues found"


    messages = [
        SystemMessage(content = REGISTRAR_SCOUT_PROMPT),
        HumanMessage(content = str(data))
    ]

    assessment = structured_llm.invoke(messages)

    summary = f"""🔍 REGISTRAR SCOUT REASONING:
    Reasoning: {assessment.reasoning}
    Red Flags: {', '.join(assessment.risk_factors) if assessment.risk_factors else 'None'}
    Assigned Score: {assessment.calculated_score}
    """


    return {
        "registry_data": data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": assessment.calculated_score
    }


# The nodes (registrar, geospatial, digital) are treated as “reporting agents,” 
# so they log their findings as HumanMessage (observations) rather than decisions.


