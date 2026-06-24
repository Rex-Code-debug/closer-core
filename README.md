# 🎯 CloserCore: Automated Sales Intelligence Engine

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-FF9900?style=for-the-badge&logo=langchain)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LLaMA](https://img.shields.io/badge/Meta_Llama_3-0466C8?style=for-the-badge)

### 🚀 Executive Summary
CloserCore is a state-aware AI orchestration engine built to maximize ROI on human capital for B2B sales teams. It transforms a manual, 2-hour data-entry bottleneck into a frictionless, multi-agent pipeline that executes in seconds.

### ⚠️ The Business Problem
Currently, sales representatives waste immense time manually researching leads. For a batch of 50 target companies, a rep spends roughly 2 hours copying URLs from a CRM, searching Google, reading raw HTML sites, and manually typing up summaries. This is highly inefficient and drains the energy reps should be using to actually close deals.

### 💡 The Automated Solution
CloserCore eliminates this friction completely. The user simply inputs a target **Company Name**. The system takes full autonomy: it identifies the correct corporate domain, concurrently scrapes the raw data, sanitizes the noise, and synthesizes a highly actionable, structured business report. **Result: A 10X boost in sales team productivity.**

### ⚙️ High-Level Architecture (Dual-LLM Pipeline)
Orchestrated via **LangGraph** and exposed as **FastAPI** microservices, the data flow ensures maximum speed and compute efficiency:
1. **Discovery:** DuckDuckGo Search (DDGS) tool autonomously maps the company name to its official URL.
2. **Ingestion:** Non-blocking, concurrent scraping utilizing `async httpx` and `BeautifulSoup` minimizes latency.
3. **Sanitization:** A highly optimized **Llama 8B** model acts as the data-cleaner, truncating raw HTML and extracting only high-value data points.
4. **Synthesis:** The concentrated payload is passed to a heavyweight **Llama 70B** model to generate the final executive report.

# 🎯 CloserCore | Agentic Competitive Intelligence Engine

**CloserCore** is a high-performance, multi-agent research system designed to automate competitive intelligence. Built with **LangGraph** and **Python**, it transforms a simple company name into a comprehensive "Battle Card" used by sales teams to outmaneuver (outperform) competitors and close deals faster.

## 🚀 Key Features
* **Autonomous Detective Node:** Automatically identifies official websites, company descriptions, and key competitors.
* **Deep-Dive Pricing Extraction:** Scrapes and parses complex pricing structures using intelligent chunking and RAG.
* **Sentiment & News Analysis:** Leverages DuckDuckGo search to find recent headlines and customer sentiment.
* **Stateful Orchestration:** Built on **LangGraph StateGraphs** to ensure fault-tolerant (error-resistant) execution and complex looping logic.
* **Markdown Generation:** Outputs professional, ready-to-use Battle Cards for Sales Ops.

## 🛠️ Technical Stack
* **Framework:** LangGraph (StateGraph)
* **Orchestration:** LangChain
* **LLM:** Llama-3.1-8b (via Groq) for ultra-fast inference
* **Data Acquisition:** BeautifulSoup4, Requests, DuckDuckGo Search
* **Environment:** Python 3.10+, Dotenv

## 📊 Logic Flow
CloserCore doesn't just run a script; it manages a stateful workflow:
1. **Research Phase** -> 2. **Pricing Extraction** -> 3. **Intelligence Gathering** -> 4. **Strategic Synthesis (LLM)** -> 5. **Final Delivery**
