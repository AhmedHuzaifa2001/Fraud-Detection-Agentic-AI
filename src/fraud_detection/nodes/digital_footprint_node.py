from src.fraud_detection.tools.web_search_tool import web_search
from src.fraud_detection.tools.risk_calculator_tool import calculate_digital_risk
from src.fraud_detection.state.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from src.fraud_detection.LLM.groqLLM import get_groq_llm
from src.fraud_detection.state.state import RegistryAgentRiskAssessment

llm = get_groq_llm()

DIGITAL_FOOTPRINT_TRACER_PROMPT = """
You are a Digital Footprint Investigator specializing in fraud detection.
I will provide raw web search and digital presence data. Your task is to evaluate the online credibility and fraud risk on a scale of 0 to 100.

EVALUATION GUIDELINES:
- Ghost Companies: 0 search results is highly suspicious (+25).
- Negative Sentiment: Keywords like 'scam', 'lawsuit', or 'fraud' are massive red flags (+40).
- Social Proof: Missing social media or a weak/non-existent LinkedIn presence indicates lack of professional footprint (+15 to +30 depending on severity).

⚠️ CRITICAL EXCEPTIONS:
If the company is a well-known, massive brand (e.g., millions of search results), but specific fields like 'linkedin_connections' return null or 0, treat this as a web-scraping tool limitation, NOT a red flag. Huge companies are inherently verified by their massive search volume.
If the search results are healthy and no explicit negative keywords or red flags are found, assign a score of 0.

Think step-by-step about the context, list the risk factors, and assign a final calculated score.
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

    structured_llm = llm.with_structured_output(RegistryAgentRiskAssessment)

    messages = [
        SystemMessage(content = DIGITAL_FOOTPRINT_TRACER_PROMPT),
        HumanMessage(content = str(digital_data))
    ]
    # negative_keywords = ", ".join(digital_data.get("negative_keywords_found", [])) if digital_data.get("negative_keywords_found") else "None"

    assessment = structured_llm.invoke(messages)

    
    summary = f"""💻 DIGITAL FOOTPRINT TRACER REASONING:
    Reasoning: {assessment.reasoning}
    Red Flags: {', '.join(assessment.risk_factors) if assessment.risk_factors else 'None'}
    Assigned Score: {assessment.calculated_score}
    """


    return {
        "web_data": digital_data,  
        "evidence_log": [HumanMessage(content=summary)],
        "risk_score": assessment.calculated_score
    }


    