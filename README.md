# 🕵️‍♂️ Fraud Detection - Agentic AI Pipeline

A sophisticated, multi-agent artificial intelligence pipeline designed to automate corporate due diligence and fraud detection. Built using **LangGraph**, **Groq (Llama Models)**, **Tavily**, and 
**OpenStreetMap**, this system investigates companies in real-time by analyzing their legal registry, physical location, and digital footprint.

---

## 🏗️ System Architecture

The pipeline operates as a directed graph where data flows sequentially through four specialized AI agents:

### 1. 🔍 Registrar Scout (Legal Verification)
- **Role:** Company Registry Investigator.
- **How it works:** Uses agentic web scraping (Tavily API) to find the company's registration details globally. It passes the raw search results to the Groq LLM with a Pydantic strict schema to extract exact JSON data.
- **Checks for:** Dissolved status, newly formed shell companies (<7 days old), missing directors, or suspicious names.

### 2. 🗺️ Geo-Spatial Analyst (Address Verification)
- **Role:** Physical Location Specialist.
- **How it works:** Takes the address discovered by the Registrar Scout and queries the **OpenStreetMap (Nominatim)** API. If the Registrar Scout couldn't find an address, it intelligently falls back to searching the map by company name.
- **Checks for:** Completely fake addresses, P.O. Boxes, UPS Stores/Mail forwarding services, or businesses operating in residential zones.

### 3. 💻 Digital Footprint Tracer (Online Presence)
- **Role:** Digital Credibility Investigator.
- **How it works:** Performs a targeted web search via Tavily to analyze the company's real-world footprint.
- **Checks for:** "Ghost" companies with zero search results, negative keywords (fraud, scam, lawsuit, investigation), and verifies the existence of professional social media (LinkedIn).

### 4. ⚖️ Supervisor (Decision Maker)
- **Role:** Investigation Coordinator.
- **How it works:** Reviews the aggregated data and the individual risk scores assigned by the three scout agents. Calculates a total risk score and issues a final, human-readable assessment.
- **Outcomes:** 
  - ✅ **Cleared** (Low Risk: 0-30)
  - ⚠️ **Pending** (Medium Risk: 31-60 - flagged for monitoring)
  - 🚨 **Escalated** (High/Critical Risk: 61+ - immediate human review)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **LangGraph** | Multi-agent orchestration and state management |
| **LangChain** | LLM framework, structured output, and message handling |
| **Groq** | Lightning-fast LLM inference (Llama-3.3-70b-versatile) |
| **Tavily API** | Real-time AI web search and data gathering |
| **Geopy / OpenStreetMap** | Open-source, keyless geospatial address verification |
| **Pydantic** | Enforcing strict JSON data schemas for the LLM |

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Clone & Install
Install the required dependencies:
```bash
pip install langgraph langchain langchain-groq python-dotenv tavily-python pydantic geopy
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY="your_groq_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

### 4. Running the Project
Currently, the pipeline is designed to be run and visualized via **LangGraph Studio**. 
Ensure your `langgraph.json` is in the root directory:
```json
{
    "dependencies": ["."],
    "graphs": {
        "fraud_detection": "./src/fraud_detection/graph/fraud_detection_graph.py:graph_builder"
    },
    "env": "./.env"
}
```
Open the project in LangGraph Studio, input a `company_name` in the state payload, and watch the agents go to work!

---

## 🔮 Future Enhancements
- **FastAPI / Streamlit Integration:** Expose the pipeline via a REST API or a web frontend so non-technical users can run investigations.
- **Vector Database (Pinecone):** Store historical investigation reports to detect repeating fraud rings or connected bad actors over time.
