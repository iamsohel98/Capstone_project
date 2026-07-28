# Group 5 Capstone Project

# Enterprise Business / Market Intelligence

## Multi-Agent Market Research and Executive Reporting Platform

---

## 1. Project Overview

This project is a **domain-based AI Engineer capstone project** for the **Enterprise Business / Market Intelligence** domain. The goal is to build a client-style AI solution that helps business teams perform market research, competitor analysis, industry trend summarization, and executive report generation using approved internal or sample research documents.

The platform uses **GenAI, Agentic AI, LangGraph, RAG, FastAPI, Streamlit, Docker, Cloud deployment design, LLMOps/MLOps, and Responsible AI controls** to deliver a complete AI engineering solution.

---

## 2. Problem Statement

Business teams often need to prepare market research summaries, competitor analysis reports, industry trend insights, and executive-level reports. This process is usually manual, time-consuming, and difficult to verify against source documents.

The proposed solution is a **Multi-Agent Market Research and Executive Reporting Platform** that can analyze sample research documents, extract key insights, verify facts, and generate executive-ready reports with citations and responsible AI safeguards.

---

## 3. Objective

The objective of this project is to collaboratively build a domain-specific AI Engineer solution using **Git and GitHub**. The system must include:

- A working AI demo
- Streamlit UI
- FastAPI backend
- Dockerfile or containerization plan
- Multi-agent AI workflow
- Architecture diagram
- Cloud deployment design
- Monitoring and logging strategy
- LLMOps/MLOps plan
- Responsible AI controls
- Final presentation covering implementation and demo

---

## 4. Domain

**Domain:** Enterprise Business / Market Intelligence  
**Project Title:** Multi-Agent Market Research and Executive Reporting Platform

---

## 5. Key Features

- Upload or use sample research documents
- Ask market intelligence questions
- Retrieve relevant information from documents
- Perform competitor analysis
- Summarize industry trends
- Verify generated insights against source documents
- Generate executive-ready business reports
- Provide citations for every important claim
- Display answer-not-found behavior when information is unavailable
- Track query count, latency, errors, token usage, and cost concept
- Support responsible AI controls and human review for high-risk outputs

---

## 6. Proposed Solution

The solution will use a **multi-agent architecture** where different agents perform specialized tasks.

### Agents Used

1. **Research Agent**
   - Retrieves information from approved or sample documents
   - Extracts market research data
   - Collects competitor and industry trend information

2. **Verifier Agent**
   - Checks whether answers are supported by retrieved sources
   - Validates citations
   - Triggers retry when facts are not properly grounded

3. **Summarizer Agent**
   - Converts retrieved information into simple business insights
   - Summarizes industry trends, risks, opportunities, and competitor insights

4. **Report Generator Agent**
   - Generates executive-ready reports
   - Structures the final output into business-friendly sections
   - Includes citations and recommendations

---

## 7. System Architecture

```text
                 +------------------+
                 |   Streamlit UI   |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 | FastAPI Backend  |
                 +--------+---------+
                          |
                          v
                    LangGraph Flow
                          |
      +-------------------+-------------------+
      |                   |                   |
      v                   v                   v
+-------------+   +-------------+   +-------------+
| Research    |-->| Verifier    |-->| Summarizer  |
| Agent       |   | Agent       |   | Agent       |
+-------------+   +-------------+   +-------------+
                          |
                          v
                 +------------------+
                 | Report Generator |
                 +------------------+
                          |
                          v
                 Executive Report
```

---

## 8. Tech Stack

### Frontend

- Streamlit
- Plotly charts for dashboard visualization

### Backend

- FastAPI
- Pydantic
- REST API endpoints

### AI / Agentic Layer

- LangGraph
- LangChain
- Azure OpenAI / AWS Bedrock / Google Vertex AI concept
- Prompt templates
- Multi-agent orchestration

### RAG / Data Layer

- Sample research documents
- ChromaDB or FAISS vector database
- Embedding model
- Document chunking and retrieval

### Deployment

- Docker
- Azure Container Apps / AWS ECS / Google Cloud Run concept

### Monitoring

- Application logs
- Query count tracking
- Latency tracking
- Error tracking
- Token usage and cost tracking concept

---

## 9. Application Workflow

1. User opens the Streamlit UI.
2. User uploads sample research documents or selects existing sample data.
3. User enters a market research query.
4. FastAPI receives the request.
5. LangGraph starts the multi-agent workflow.
6. Research Agent retrieves relevant information from documents.
7. Verifier Agent validates facts and citations.
8. Summarizer Agent prepares business insights.
9. Report Generator Agent creates the final executive report.
10. User views the final report in the UI and downloads it if required.

---

## 10. Sample User Queries

- What are the top market trends in Generative AI?
- Compare Company A and Company B based on innovation and market position.
- Summarize the latest industry opportunities from the uploaded documents.
- Generate an executive report on AI adoption in enterprise business.
- Identify risks and recommendations from the research documents.

---

## 11. FastAPI Endpoints

```text
GET  /health
POST /research
POST /generate-report
GET  /logs
GET  /metrics
```

### Endpoint Description

| Endpoint | Purpose |
|---|---|
| `/health` | Checks whether the backend is running |
| `/research` | Accepts user query and returns retrieved insights |
| `/generate-report` | Generates executive report using agent workflow |
| `/logs` | Displays basic application logs |
| `/metrics` | Displays query count, latency, errors, and token usage concept |

---

## 12. Streamlit UI Pages

### 1. Home Page

- Project title
- Domain introduction
- Upload sample documents
- Enter research query

### 2. Research Dashboard

- Display retrieved sources
- Display agent workflow status
- Show key findings

### 3. Executive Report Page

- Executive summary
- Industry overview
- Competitor analysis
- Market opportunities
- Risks and recommendations
- Citations and references

### 4. Monitoring Dashboard

- Query count
- Latency
- Errors
- Token usage concept
- Cost tracking concept

---

## 13. Responsible AI Controls

The project includes the following Responsible AI controls:

- Use only sample or synthetic data
- Do not use confidential client or participant data
- Provide citations for generated answers
- Return answer-not-found response when sources do not contain enough information
- Avoid unsupported claims
- Add privacy and access-control design
- Maintain audit logs
- Add human review for high-risk business reports
- Clearly separate AI-generated content from verified source-based content

---

## 14. LLMOps / MLOps Strategy

### Prompt Versioning

All prompts will be versioned to track improvements.

Example:

```text
prompt_v1.0_basic_summary
prompt_v1.1_with_citations
prompt_v2.0_with_verifier_loop
```

### Evaluation Dataset

A small evaluation dataset will be prepared using sample research questions and expected answers.

### Evaluation Metrics

- Relevance
- Groundedness
- Citation coverage
- Hallucination rate
- Response completeness
- User feedback score

### Feedback Loop

```text
User Feedback
      ↓
Evaluation
      ↓
Prompt Improvement
      ↓
Regression Testing
      ↓
Updated Deployment
```

---

## 15. Monitoring and Logging Strategy

The platform will track:

- Total number of user queries
- API response latency
- Application errors
- Retrieved source documents
- Token usage concept
- Estimated cost concept
- User feedback
- Failed verification attempts

These logs will help improve system reliability, quality, and traceability.

---

## 16. Dockerization Plan

The project will include a Dockerfile to containerize the application.

### Example Docker Commands

```bash
docker build -t market-intelligence-ai .
docker run -p 8000:8000 market-intelligence-ai
```

---

## 17. Suggested Project Folder Structure

```text
market-intelligence-ai/
│
├── frontend/
│   └── app.py
│
├── backend/
│   └── main.py
│
├── agents/
│   ├── research_agent.py
│   ├── verifier_agent.py
│   ├── summarizer_agent.py
│   └── report_generator_agent.py
│
├── workflows/
│   └── langgraph_workflow.py
│
├── data/
│   └── sample_documents/
│
├── vectorstore/
│
├── prompts/
│   ├── research_prompt.txt
│   ├── verifier_prompt.txt
│   └── report_prompt.txt
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── requirements.txt
├── README.md
└── architecture_diagram.png
```

---

## 18. GitHub Collaboration Plan

All team members will collaborate using Git and GitHub.

### Git Practices

- Create feature branches
- Write meaningful commit messages
- Raise pull requests
- Add code review comments
- Maintain clean README documentation
- Track tasks using GitHub Issues or project board

### Example Branch Names

```text
feature/streamlit-ui
feature/fastapi-backend
feature/rag-pipeline
feature/langgraph-agents
feature/docker-deployment
feature/monitoring-logging
```

---

## 19. Team Responsibility Distribution

| Member | Responsibility |
|---|---|
| Member 1 | Streamlit UI and user experience |
| Member 2 | FastAPI backend and API integration |
| Member 3 | RAG pipeline and vector database |
| Member 4 | LangGraph multi-agent workflow |
| Member 5 | Docker, cloud deployment design, and architecture diagram |
| Member 6 | Monitoring, logging, README, and final presentation |

---

## 20. Final Presentation Structure

The final presentation should include:

1. Project title and team details
2. Problem statement
3. Business objective
4. Proposed solution
5. Architecture diagram
6. Tech stack
7. Multi-agent workflow
8. Implementation details
9. Demo screenshots
10. Monitoring and logging strategy
11. LLMOps/MLOps strategy
12. Responsible AI controls
13. Challenges faced
14. Future scope
15. Conclusion

---

## 21. Challenges

Possible project challenges include:

- Designing accurate retrieval from documents
- Reducing hallucination in generated reports
- Ensuring every important claim has citations
- Coordinating multiple agents using LangGraph
- Preparing proper monitoring and evaluation strategy
- Maintaining clean Git collaboration between all group members

---

## 22. Future Scope

Future improvements can include:

- Real-time integration with approved market research APIs
- Advanced dashboard with business KPIs
- Role-based access control
- Automated PDF and PowerPoint report generation
- Integration with Microsoft Teams or email workflow
- Advanced evaluation using larger benchmark datasets
- Human feedback-based continuous improvement

---

## 23. Expected Deliverables

- GitHub repository
- Clean README file
- Streamlit UI
- FastAPI backend
- LangGraph multi-agent workflow
- RAG pipeline using sample documents
- Dockerfile
- Architecture diagram
- Cloud deployment design
- Monitoring and logging strategy
- LLMOps/MLOps strategy
- Responsible AI controls
- Final presentation deck
- Working AI demo

---

## 24. Conclusion

The **Multi-Agent Market Research and Executive Reporting Platform** is a strong capstone project because it combines real-world business value with modern AI engineering practices. It demonstrates skills in GenAI, Agentic AI, LangGraph, RAG, FastAPI, Streamlit, Docker, cloud deployment design, monitoring, LLMOps/MLOps, and Responsible AI.

This project can help business teams save time, improve research quality, verify insights, and generate executive-ready reports using AI in a safe and responsible way.
