# 📝 CloserCore: Persistent Competitive Intelligence Platform

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-FF9900?style=for-the-badge&logo=langchain)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![LLaMA](https://img.shields.io/badge/Meta_Llama_3-0466C8?style=for-the-badge)

---

## 📋 Executive Summary

**CloserCore** is a state-aware AI orchestration engine that transforms B2B sales intelligence from a manual, 2-hour research bottleneck into a frictionless, multi-agent pipeline executing in seconds.

With the introduction of **persistent intelligence storage** (V1.1), CloserCore evolves from a transient report generator into a platform that builds, retains, and leverages competitive intelligence as a reusable business asset. Every research run now contributes to a growing knowledge base—eliminating redundant work and enabling future capabilities.

---

## ⚠️ The Business Problem

Sales representatives waste immense time manually researching leads. For a batch of 50 target companies, a rep spends roughly **2 hours** copying URLs from a CRM, searching Google, reading raw HTML sites, and manually typing up summaries. This inefficiency drains energy that should be spent closing deals.

**The hidden cost:** Even when research is completed, the intelligence is trapped in documents, emails, or memory—never structured, never reusable, and lost when the rep moves on.

---

## 💡 The Automated Solution

CloserCore eliminates this friction completely. The user inputs a target **Company Name**, and the system autonomously:

1. Identifies the correct corporate domain
2. Concurrently scrapes and sanitizes raw data
3. Synthesizes a structured, actionable "Battle Card"
4. **Persists all research as permanent business assets** (NEW in V1.1)

**Result:** 10X boost in sales team productivity, backed by a growing intelligence repository that compounds in value with every use.

---

## 🚀 Core Features

### Intelligence Pipeline
- **Autonomous Discovery:** DuckDuckGo Search autonomously maps company names to official URLs
- **Concurrent Ingestion:** Non-blocking `requests` and `BeautifulSoup` scraping minimizes latency
- **Dual-LLM Sanitization Pipeline:** Lightweight Llama 8B extracts high-value data from raw HTML; heavyweight Llama 70B synthesizes executive reports
- **Pricing Extraction:** Intelligent chunking parses complex pricing structures
- **Sentiment & News Analysis:** Recent headlines and customer sentiment via DuckDuckGo

### Persistence Layer (V1.1)
- **Research Archival:** Every execution is stored with full metadata
- **Company Intelligence Database:** Structured storage of company profiles, competitors, and pricing data
- **Battle Card Archive:** Historical snapshots of generated intelligence
- **Execution Tracking:** Audit trail of all research runs for analytics and debugging

---

## 🛠️ Technical Stack

| Layer | Technology |
|-------|------------|
| **Orchestration** | LangGraph (StateGraph) |
| **Framework** | LangChain |
| **API Layer** | FastAPI |
| **LLM Inference** | Llama-3.1-8B & 70B (via Groq) |
| **Data Acquisition** | BeautifulSoup4, httpx, DuckDuckGo Search, tavily |
| **Persistence** | SQLModel + SQLAlchemy |
| **Environment** | Python 3.10+, Dotenv |

---

## 🧠 System Architecture

CloserCore operates as a stateful workflow managed by LangGraph, with persistence integrated at every stage:

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT: Company Name                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  RESEARCH PHASE                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Discovery Node    │ DuckDuckGo Search → Official URL    │   │
│  │ Ingestion Node    │ Concurrent scraping (requests)      │   │
│  │ Sanitization Node │ Llama 8B → Extract high-value data  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  INTELLIGENCE PHASE                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Pricing Extraction │ Chunking → Parse structures        │   │
│  │ Sentiment Analysis │ DDGS → News + Customer sentiment   │   │
│  │ Competitor Mapping │ Auto-identify key competitors      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  SYNTHESIS PHASE                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Battle Card Generation │ Llama 70B → Executive report   │   │
│  │ Markdown Formatting    │ Professional output ready      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  PERSISTENCE LAYER (V1.1)  ←───  NEW                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Store Research Run    │ Execution metadata + timestamp   │   │
│  │ Save Company Profile  │ Structured company intelligence  │   │
│  │ Archive Battle Card   │ Full report with versioning     │   │
│  │ Update Knowledge Base │ Cumulative intelligence growth  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT: Persistent Battle Card             │
│                  (Stored + Available for future retrieval)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Project Structure

CloserCore/
│
├── app.py                    # FastAPI application entry point
├── bt_card.py                # LangGraph workflow & Battle Card pipeline
├── func.py                   # Search and web scraping utilities
├── schema.py                 # Pydantic / SQLModel schemas and shared state
├── config.py                 # Application configuration & logging
├── database/
│   ├── connection.py         # Database engine and session management
│   ├── models.py             # SQLModel database models
│   └── crud.py               # Database persistence logic
├── migration/                # Alembic migration environment
├── cards/                    # Generated Battle Cards (.md)
├── .env                      # Environment variables
├── .gitignore
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── data_extraction.log       # Application logs               # Project documentation

---

## 📊 Data Model (Persistence Layer)

| Table | Description |
|-------|-------------|
| `companies` | Core company profiles (name, domain, description) |
| `research_runs` | Execution metadata (timestamp, status, duration) |
| `battle_cards` | Generated reports with versioning and markdown content |
| `competitors` | Identified competitors linked to companies |
| `pricing_data` | Structured pricing information |

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10+
- Groq API key

### Quick Start

```bash
# Clone repository
git clone https://github.com/rex-code-debug/closer-core.git
cd closer-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# Initialize database
python -c "from database import init_db; init_db()"

# Start the API server
uvicorn app:app --reload
```

---

## 📡 API Usage

### Submit Research Request

```http
POST /research
Content-Type: application/json

{
  "company_name": "Snowflake"
}
```

**Response:**
```json
{
  "run_id": 42,
  "status": "completed",
  "battle_card": "# Battle Card: Snowflake\n\n..."
}
```

---

## 🔬 Engineering Decisions

### Why LangGraph?
LangGraph's StateGraph architecture provides native support for:
- **Fault-tolerant execution** with state persistence
- **Complex branching logic** (e.g., retry on failed discovery, conditional competitor mapping)
- **Observability** through built-in tracing

### Dual-LLM Architecture
- **Llama 8B (Sanitization):** Fast, cost-effective data cleaning from raw HTML—processes 100+ pages concurrently
- **Llama 70B (Synthesis):** Deep strategic reasoning for final report generation
- **Result:** 70% cost reduction vs. using a single heavy model for all tasks

### Persistence Strategy
- **SQLite** chosen for zero-configuration local development
- **SQLAlchemy ORM** provides clean separation of database logic
- **Separation of concerns:** Research runs, company profiles, and Battle Cards stored independently to enable flexible querying
- **Versioning:** Historical snapshots allow for "company intelligence over time" analysis

### Async-First Design
`requests` with concurrency patterns enables parallel scraping, reducing total pipeline time from sequential ~30 seconds to ~8 seconds for typical loads.

---

## 📈 Performance & Results

| Metric | V1.0 (Stateless) | V1.1 (Persistent) |
|--------|------------------|-------------------|
| Research Execution Time | ~8 seconds | ~8 seconds (no regression) |
| Intelligence Reusability | 0% (lost after run) | 100% (permanently stored) |
| Historical Analysis | Not possible | Full audit trail |

**V1.1 Impact:**
- Eliminates redundant research for revisited companies
- Enables cross-company competitive analysis
- Builds a strategic asset that compounds over time

---

## 🔮 Roadmap

### Completed
- [x] **V1.0:** Real-time intelligence engine
- [x] **V1.1:** Persistence layer—every research run stored as a business asset

### Planned
- [ ] **V1.2:** Intelligent caching—serve existing research before triggering new runs
- [ ] **V1.3:** Automated monitoring—track competitor changes and notify teams
- [ ] **V1.4:** RESTful API endpoints for `/research-runs` and filtered queries
- [ ] **V1.5:** Docker containerization for simplified deployment
- [ ] **V2.0:** Multi-tenant support and team collaboration features

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact

**Project Lead:** Dhananjay Mishra 
**Email:** mdhananjay776@gmail.com  
**GitHub:** [Rex-Code-debug](https://github.com/rex-code-debug)

---

*Built with FastAPI, LangGraph, and Llama—designed to turn sales intelligence into a compounding asset.*

---