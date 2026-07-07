# 🕵️‍♂️ Fraud Detection — Agentic AI Pipeline

A sophisticated, multi-agent artificial intelligence system that automates corporate due diligence and fraud detection in real-time. Built on **LangGraph**, the pipeline orchestrates a team of specialized AI agents that independently investigate a company's legal registry, physical location, and digital footprint — then aggregate their findings into a unified risk assessment.

> **What makes this project unique:** Every agent uses **LLM-centered reasoning** with Pydantic structured output to assign risk scores. Instead of relying on hard-coded Python `if/else` rules, each agent thinks step-by-step, lists its red flags, and assigns a calculated score — just like a real human fraud analyst would.

---

## 🏗️ System Architecture

```
                        ┌──────────────────────┐
                        │      __start__        │
                        │  (company_name input) │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Registrar Scout Node │
                        │  (Legal Verification) │
                        └──────────┬───────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │ (Parallel Execution - Fan Out)│
                    ▼                              ▼
       ┌────────────────────┐         ┌─────────────────────┐
       │ Geo-Spatial Analyst │         │ Digital Footprint    │
       │ (Address Verify)    │         │ Tracer (Web Scan)    │
       └─────────┬──────────┘         └──────────┬──────────┘
                 │                                │
                 └──────────────┬─────────────────┘
                                │ (Fan In - Scores Accumulated)
                     ┌──────────▼───────────┐
                     │   Supervisor Node     │
                     │   (Final Decision)    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  Conditional Router   │
                     │  (Cleared → END)      │
                     │  (Pending/Escalated   │
                     │   → Human Analyst)    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  Human Analyst Node   │
                     │  (Human-in-the-Loop)  │
                     └──────────┬───────────┘
                                │
                            __end__
```

### Key Architectural Features

- **Parallel Execution:** After the Registrar Scout completes, the Geospatial Analyst and Digital Footprint Tracer run **simultaneously** (fan-out), dramatically reducing total investigation time.
- **Automatic Score Accumulation:** The `risk_score` field in the state uses LangGraph's `operator.add` reducer, so each agent's score is automatically summed as data flows through the graph — no manual calculation needed.
- **Conditional Routing:** The Supervisor dynamically routes the investigation to either `END` (if cleared) or a `Human Analyst Node` (if pending/escalated).

---

## 🤖 Agent Breakdown

### 1. 🔍 Registrar Scout (Legal Verification)
- **Role:** Company Registry Investigator
- **Data Source:** Agentic web scraping via **Tavily API** → structured extraction via **Groq LLM** with Pydantic schema (`RegistryData`)
- **How it works:** Searches the web for the company's corporate details, then forces the LLM to extract exact JSON fields (exists, incorporation_date, status, directors, address, jurisdiction). The LLM then reasons about the data step-by-step and assigns a risk score (0–100).
- **Red Flags Detected:** Dissolved/inactive status, brand-new shell companies (<7 days old), missing or suspicious director names (e.g., "John Doe"), non-existent companies.

### 2. 🗺️ Geo-Spatial Analyst (Address Verification)
- **Role:** Physical Location Specialist
- **Data Source:** **OpenStreetMap (Nominatim)** via `geopy` — no API key required
- **How it works:** Takes the address from the Registrar Scout (or falls back to company name if address is missing) and queries OpenStreetMap for real-world coordinates and location classification. The LLM then evaluates the geospatial data and assigns a risk score.
- **Fallback Strategy (3 layers):**
  1. Real OpenStreetMap API lookup
  2. Mock address database (for testing known scenarios like P.O. Boxes)
  3. String pattern analysis (detects "P.O. Box", "UPS Store" keywords)
- **Red Flags Detected:** Unverified addresses, P.O. Boxes, UPS Stores/mail forwarding, empty lots, zoning mismatches.

### 3. 💻 Digital Footprint Tracer (Online Presence)
- **Role:** Digital Credibility Investigator
- **Data Source:** **Tavily API** for real-time web search
- **How it works:** Performs a targeted web search for the company, scans for negative sentiment keywords, checks for social media presence across major platforms, and extracts LinkedIn profile URLs. The LLM evaluates the digital evidence and assigns a risk score.
- **Red Flags Detected:** Ghost companies (0 search results), negative keywords ("fraud", "scam", "lawsuit", "investigation"), missing social media, no LinkedIn presence.

### 4. ⚖️ Supervisor (Decision Maker)
- **Role:** Investigation Coordinator
- **How it works:** Reads the accumulated `risk_score` from the state (automatically summed by `operator.add`), determines the risk level, and generates a final assessment via the LLM. Routes the case based on risk severity.
- **Decision Outcomes:**
  | Risk Score | Level | Action |
  |---|---|---|
  | 0–30 | ✅ Low | Company **cleared** → Investigation ends |
  | 31–60 | ⚠️ Medium | **Pending** → Routed to Human Analyst |
  | 61–90 | 🔴 High | **Escalated** → Routed to Human Analyst |
  | 91+ | 🚨 Critical | **Escalated** → Immediate human review |

### 5. 👨‍💼 Human Analyst (Human-in-the-Loop)
- **Role:** Manual Review Placeholder
- **How it works:** Only triggered when the Supervisor flags a case as "pending" or "escalated". Logs the case to a manual review queue for a human investigator to approve or reject.

---

## 🧠 LLM-Centered Risk Scoring

Each scout agent uses **LangChain Structured Output** with the `RegistryAgentRiskAssessment` Pydantic schema:

```python
class RegistryAgentRiskAssessment(BaseModel):
    reasoning: str       # Step-by-step Chain-of-Thought explanation
    risk_factors: list[str]  # Specific red flags found
    calculated_score: int    # Final risk score (0–100)
```

This approach provides:
- **Explainability:** Every score comes with a written justification.
- **Adaptability:** The LLM can handle edge cases (brand names vs. legal names, famous companies with missing data) that rigid rules cannot.
- **Auditability:** The `evidence_log` preserves the full reasoning chain for every agent.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **LangGraph** | Multi-agent orchestration, state management, parallel execution |
| **LangChain** | LLM framework, structured output, message handling |
| **Groq** | Ultra-fast LLM inference (Llama 3.3 70B / GPT-OSS 120B) |
| **Tavily API** | Real-time AI-powered web search and data gathering |
| **Geopy / OpenStreetMap** | Open-source, keyless geospatial address verification |
| **Pydantic** | Enforcing strict JSON schemas for LLM extraction and reasoning |

---

## 📁 Project Structure

```
Fraud_Detection/
├── app.py                          # Application entry point (TBD)
├── langgraph.json                  # LangGraph Studio configuration
├── .env                            # API keys (GROQ_API_KEY, TAVILY_API_KEY)
└── src/
    └── fraud_detection/
        ├── main.py                 # CLI entry point (TBD)
        ├── graph/
        │   └── fraud_detection_graph.py   # StateGraph definition & compilation
        ├── state/
        │   └── state.py            # AgentState (TypedDict) + Pydantic schemas
        ├── nodes/
        │   ├── registrar_scout_node.py       # Agent A: Legal verification
        │   ├── geospatial_analyst_node.py    # Agent B: Address verification
        │   ├── digital_footprint_node.py     # Agent C: Online presence
        │   ├── supervisor_node.py            # Agent D: Decision maker
        │   └── human_analyst_node.py         # Agent E: Human-in-the-loop
        ├── tools/
        │   ├── registry_lookup_tool.py       # Tavily + LLM structured extraction
        │   ├── geospatial_tool.py            # OpenStreetMap + mock fallback
        │   ├── web_search_tool.py            # Tavily search + mock fallback
        │   └── risk_calculator_tool.py       # Rule-based calculators (legacy)
        ├── LLM/
        │   └── groqLLM.py          # Groq LLM initialization
        └── api/
            └── pydantic_model/     # API schemas (TBD)
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com/) (free tier available)
- A [Tavily API key](https://tavily.com/) (free tier: 1,000 searches/month)

### 2. Install Dependencies
```bash
pip install langgraph langchain langchain-groq python-dotenv tavily-python pydantic geopy
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

### 4. Run with LangGraph Studio
Ensure your `langgraph.json` is in the project root:
```json
{
    "dependencies": ["."],
    "graphs": {
        "fraud_detection": "./src/fraud_detection/graph/fraud_detection_graph.py:graph_builder"
    },
    "env": "./.env"
}
```
Open the project in **LangGraph Studio**, input a `company_name` (e.g., `"Google"`, `"Tesla"`, `"Acme Corp"`), and watch the agents investigate in real-time!

---

## 🧪 Example Results

### Searching for "Google"
| Agent | Score | Key Finding |
|---|---|---|
| Registrar Scout | 0 | Active company, incorporated 1998-09-04, HQ: 1600 Amphitheatre Parkway |
| Geo-Spatial Analyst | 0 | Address verified via OpenStreetMap, classified as "Building" |
| Digital Footprint | 0 | 9+ search results, LinkedIn found, no negative keywords |
| **Supervisor** | **0** | **✅ CLEARED — Low risk** |

### Searching for a Suspicious Company
| Agent | Score | Key Finding |
|---|---|---|
| Registrar Scout | 100 | Company not found in any registry |
| Geo-Spatial Analyst | 50 | Address could not be verified |
| Digital Footprint | 40 | Zero online presence, no social media |
| **Supervisor** | **190** | **🚨 ESCALATED — Critical risk → Human Analyst** |

---

## 🔮 Future Enhancements
- **Streamlit / FastAPI Integration:** Expose the pipeline via a web UI or REST API for non-technical users.
- **Vector Database (Pinecone):** Store historical investigation reports to detect repeating fraud rings or connected bad actors over time.
- **Director Cross-Referencing:** Use the Digital Footprint Tracer to independently verify each director's identity.
- **PDF Report Generation:** Auto-generate downloadable investigation reports for compliance teams.
