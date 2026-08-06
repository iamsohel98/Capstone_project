"""
Generates a project justification PDF for the Market Intelligence capstone.
Run: python data/generate_project_justification_pdf.py
"""

from fpdf import FPDF, XPos, YPos
from pathlib import Path

OUTPUT_PATH = Path("Project_Justification_Report.pdf")


class JustificationPDF(FPDF):
    def header(self):
        self.set_fill_color(28, 64, 126)
        self.rect(0, 0, self.w, 16, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 10, "Enterprise Business / Market Intelligence - Capstone Justification Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 10, f"Page {self.page_no()} | Group 5 Capstone Project", align="C")

    def title_page(self):
        self.add_page()
        self.ln(20)
        self.set_text_color(28, 64, 126)
        self.set_font("Helvetica", "B", 22)
        self.set_x(self.l_margin)
        self.multi_cell(0, 12, "Enterprise Business / Market Intelligence", align="C")
        self.set_font("Helvetica", "B", 16)
        self.set_x(self.l_margin)
        self.multi_cell(0, 10, "Multi-Agent Market Research and Executive Reporting Platform", align="C")
        self.ln(10)
        self.set_text_color(70, 70, 70)
        self.set_font("Helvetica", "", 12)
        self.set_x(self.l_margin)
        self.multi_cell(0, 8, "Project Justification, Functional Explanation, Architecture Walkthrough, and Capstone Defense Report", align="C")
        self.ln(18)
        self.set_fill_color(235, 241, 255)
        self.set_draw_color(28, 64, 126)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 10, "Prepared For: Capstone Evaluation Panel", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)
        self.cell(0, 10, "Prepared By: Group 5", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)
        self.cell(0, 10, "Technology Stack: Streamlit, FastAPI, Azure OpenAI, LangGraph, RAG, ChromaDB, Docker", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)
        self.ln(12)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 7, "This document explains the complete business logic, technical implementation, AI workflow, RAG pipeline, backend and frontend design, deployment approach, security considerations, testing strategy, demo readiness, and submission justification for the capstone project.", align="C")

    def section(self, title):
        self.ln(3)
        self.set_fill_color(28, 64, 126)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def subsection(self, title):
        self.ln(2)
        self.set_text_color(28, 64, 126)
        self.set_font("Helvetica", "B", 10.5)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, title)
        self.set_text_color(0, 0, 0)

    def para(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.6, text)
        self.ln(1)

    def bullets(self, items):
        self.set_font("Helvetica", "", 9.5)
        for item in items:
            self.set_x(self.l_margin)
            self.cell(5, 5.6, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_x(self.l_margin + 5)
            self.multi_cell(0, 5.6, item)
        self.ln(1)

    def table(self, rows, widths):
        self.set_font("Helvetica", "", 8.5)
        for row_index, row in enumerate(rows):
            self.set_fill_color(230, 238, 255 if row_index == 0 else 255)
            fill = row_index == 0
            if row_index == 0:
                self.set_font("Helvetica", "B", 8.5)
            else:
                self.set_font("Helvetica", "", 8.5)
            x = self.get_x()
            y = self.get_y()
            heights = []
            for value, width in zip(row, widths):
                lines = self.multi_cell(width, 5, str(value), border=0, split_only=True)
                heights.append(max(6, len(lines) * 5))
            row_height = max(heights)
            if y + row_height > self.page_break_trigger:
                self.add_page()
                x = self.get_x()
                y = self.get_y()
            for value, width in zip(row, widths):
                self.set_xy(x, y)
                self.multi_cell(width, 5, str(value), border=1, fill=fill)
                x += width
            self.set_xy(self.l_margin, y + row_height)
        self.ln(2)


def add_content(pdf: JustificationPDF):
    pdf.add_page()
    pdf.section("1. Executive Summary")
    pdf.para("The project is a domain-specific AI engineering solution for Enterprise Business / Market Intelligence. It helps business teams upload approved market research documents, ask research questions, retrieve grounded evidence, verify claims, summarize insights, and generate executive-ready reports with citations.")
    pdf.para("The project is not a simple chatbot. It is a multi-agent, RAG-based decision support platform where each output is controlled by retrieval, verification, summarization, and report generation stages. The business value is faster research preparation, improved traceability, reduced hallucination risk, and reusable reporting automation.")

    pdf.section("2. Business Requirements")
    pdf.subsection("Objective")
    pdf.para("Automate market research, competitor analysis, trend summarization, and executive report generation using approved or sample documents.")
    pdf.subsection("Expected Functionality")
    pdf.bullets([
        "Allow users to upload PDF, DOCX, and TXT research documents.",
        "Retrieve relevant information from source documents using semantic search.",
        "Generate grounded business answers with citations.",
        "Verify claims against retrieved source excerpts before presenting results.",
        "Generate executive reports with structured business sections.",
        "Track query count, latency, errors, and cost concept metrics.",
    ])
    pdf.subsection("Key Features")
    pdf.bullets([
        "Business research automation for analysts and managers.",
        "Competitor analysis support using sample vendor reports.",
        "Responsible AI behavior through answer-not-found and verification logic.",
        "Downloadable executive reports for business presentation use.",
    ])

    pdf.section("3. Functional Requirements")
    pdf.table([
        ["Requirement", "Implementation", "Status"],
        ["Document upload", "FastAPI /upload-document saves and ingests files", "Implemented"],
        ["Research query", "FastAPI /research runs research graph", "Implemented"],
        ["Executive report", "FastAPI /generate-report runs report graph", "Implemented"],
        ["Monitoring", "FastAPI /metrics and Streamlit dashboard", "Implemented"],
        ["Logs", "FastAPI /logs endpoint and Loguru logging", "Implemented"],
        ["API documentation", "Swagger UI automatically available at /docs", "Implemented"],
    ], [46, 95, 35])

    pdf.section("4. User Stories")
    pdf.bullets([
        "As a business analyst, I want to upload market research documents so that I can ask questions from approved sources.",
        "As a market intelligence user, I want to ask competitor comparison questions so that I can understand vendor positioning quickly.",
        "As an executive, I want a structured report so that I can review findings without reading long source documents.",
        "As an IT/operations user, I want monitoring metrics so that I can track usage, errors, and latency.",
        "As a responsible AI reviewer, I want citations and verification flags so that I can trust the generated output.",
    ])

    pdf.section("5. System Architecture")
    pdf.para("The system follows a layered architecture: Streamlit frontend, FastAPI backend, LangGraph orchestration, four AI agents, ChromaDB vector store, Azure OpenAI chat and embedding models, and Docker-based deployment support.")
    pdf.bullets([
        "Streamlit handles user interaction and visualization.",
        "FastAPI exposes REST endpoints and handles request validation.",
        "LangGraph controls the agent workflow and retry routing.",
        "ChromaDB stores vector embeddings for semantic retrieval.",
        "Azure OpenAI provides chat completion and embedding generation.",
        "Dockerfile and docker-compose package backend and frontend services.",
    ])
    pdf.para("The architecture diagram is available in the project root as architecture_diagram.png.")

    pdf.section("6. Multi-Agent Architecture")
    pdf.table([
        ["Agent", "Purpose", "Output"],
        ["Research Agent", "Retrieves document chunks and generates grounded raw insights", "raw_insights, sources"],
        ["Verifier Agent", "Checks whether generated claims are supported by sources", "verified, verification_note"],
        ["Summarizer Agent", "Converts raw insights into business-friendly summary", "summary"],
        ["Report Generator Agent", "Creates executive report with citations and recommendations", "report, citations"],
    ], [45, 95, 40])
    pdf.para("The workflow includes conditional retry logic. If the verifier marks the answer as unverified and retry_count is less than one, the system reruns the research step once before moving forward.")

    pdf.section("7. RAG Pipeline")
    pdf.subsection("Objective")
    pdf.para("Ensure the AI answers are grounded in uploaded documents instead of relying on model memory.")
    pdf.subsection("Implementation")
    pdf.bullets([
        "Documents are loaded using PyPDFLoader, Docx2txtLoader, or TextLoader.",
        "Text is split into chunks using RecursiveCharacterTextSplitter with chunk size 800 and overlap 100.",
        "Chunks are embedded using Azure OpenAI text-embedding-3-small.",
        "Vectors and metadata are stored in ChromaDB under the vectorstore directory.",
        "User queries are embedded and compared to stored vectors to retrieve the most relevant chunks.",
        "Retrieved chunks are passed to the LLM as context for answer generation.",
    ])
    pdf.subsection("Key Feature")
    pdf.para("The platform supports live ingestion after upload. A newly uploaded document is indexed immediately and becomes available for research queries.")

    pdf.section("8. API Design")
    pdf.table([
        ["Endpoint", "Method", "Functionality"],
        ["/health", "GET", "Checks backend service health"],
        ["/research", "POST", "Runs research workflow and returns insights, sources, verification status"],
        ["/generate-report", "POST", "Runs full report workflow and returns report plus citations"],
        ["/upload-document", "POST", "Uploads and indexes PDF, DOCX, or TXT document"],
        ["/metrics", "GET", "Returns total queries, errors, latency, and cost concept"],
        ["/logs", "GET", "Returns recent application logs"],
    ], [45, 28, 107])
    pdf.para("FastAPI and Pydantic provide request validation, response schemas, error handling, and automatic Swagger documentation.")

    pdf.section("9. Frontend Implementation")
    pdf.table([
        ["Page", "Functionality"],
        ["Home", "Shows project introduction, upload control, and quick research query"],
        ["Research Dashboard", "Displays insights, sources, verified badge, latency, and request ID"],
        ["Executive Report", "Generates full report, displays citations, and supports PDF download"],
        ["Monitoring Dashboard", "Shows metrics, simulated latency trend, and recent logs"],
    ], [50, 130])
    pdf.para("The Streamlit UI acts as the user-facing business application. It calls FastAPI endpoints using HTTP requests and displays results in a simple dashboard format.")

    pdf.section("10. Backend Implementation")
    pdf.bullets([
        "FastAPI app is created with title, description, and version metadata.",
        "CORS middleware allows frontend-backend communication.",
        "Each request receives a UUID request_id for traceability.",
        "Latency is measured using time.time() and returned in milliseconds.",
        "Errors are logged and converted to HTTP 500 responses.",
        "MetricsStore tracks query count, errors, latency, and estimated cost concept.",
    ])

    pdf.section("11. Azure Integration")
    pdf.bullets([
        "Azure OpenAI endpoint and API key are loaded from .env.",
        "Chat model deployment is used by Research, Verifier, Summarizer, and Report Generator agents.",
        "Embedding deployment is used by the ingestion pipeline and vector retrieval.",
        "The current implementation uses ChromaDB as the vector store. Azure AI Search is part of the target architecture but not fully implemented in code.",
        "For production Azure deployment, Azure Container Apps, Azure Key Vault, Azure Monitor, and Azure AI Search should be added.",
    ])

    pdf.section("12. Security")
    pdf.subsection("Implemented Controls")
    pdf.bullets([
        "Secrets are externalized through .env and .env.example.",
        ".env is excluded from Git through .gitignore.",
        "Docker container runs under a non-root appuser.",
        "File upload validates PDF, DOCX, and TXT formats.",
        "Source citations and verifier agent reduce hallucination risk.",
    ])
    pdf.subsection("Current Risks")
    pdf.bullets([
        "CORS is open to all origins and should be restricted in production.",
        "No API authentication is currently implemented.",
        "No rate limiting is implemented, which can increase LLM cost exposure.",
        "SSL verification is disabled in the local OpenAI client to support corporate proxy conditions. This should be replaced by proper certificate configuration for production.",
        "No maximum upload file size is enforced.",
    ])

    pdf.section("13. Scalability")
    pdf.bullets([
        "The backend is mostly stateless and can be scaled horizontally.",
        "Dockerfile runs Uvicorn with two workers for production-style execution.",
        "Data and vectorstore directories are mounted as volumes in docker-compose.",
        "Current ChromaDB setup is suitable for capstone and small datasets but not enterprise-scale distributed search.",
        "For cloud scalability, replace ChromaDB with Azure AI Search and use Azure Container Apps autoscaling.",
    ])

    pdf.section("14. Error Handling")
    pdf.bullets([
        "FastAPI returns HTTP 400 for unsupported file types.",
        "Pydantic returns HTTP 422 for invalid request payloads.",
        "Agent exceptions are captured and propagated in workflow state.",
        "Research agent returns answer-not-found behavior when no answer is available.",
        "Verifier agent returns unverified status when no sources are available.",
        "Backend logs request failures and increments error metrics.",
    ])

    pdf.section("15. Testing Coverage")
    pdf.para("The project includes API-level unit tests using FastAPI TestClient and pytest. The tests validate health, metrics, logs, research success, research error handling, missing query validation, report generation, invalid upload, and valid TXT upload.")
    pdf.subsection("Missing Tests")
    pdf.bullets([
        "Agent-level unit tests for Research, Verifier, Summarizer, and Report Generator.",
        "LangGraph workflow tests for retry behavior.",
        "RAG ingestion tests for PDF/DOCX/TXT chunking and metadata.",
        "Frontend interaction tests.",
        "End-to-end test using a sample document and mocked Azure OpenAI responses.",
    ])

    pdf.section("16. Demo Script")
    pdf.bullets([
        "Start backend: uvicorn backend.main:app --reload --port 8000",
        "Start frontend: streamlit run frontend/app.py --server.port 8501",
        "Open Streamlit UI at http://localhost:8501.",
        "Upload sample PDFs from data/sample_documents.",
        "Run query: What are the top market trends in Generative AI?",
        "Show retrieved sources and verified badge.",
        "Generate executive report on AI adoption in enterprise business.",
        "Download the generated PDF report.",
        "Show Monitoring Dashboard and API docs at http://localhost:8000/docs.",
    ])

    pdf.section("17. Go / No-Go Assessment")
    pdf.table([
        ["Area", "Verdict", "Reason"],
        ["Demo Readiness", "GO", "Frontend, backend, agents, RAG pipeline, and sample PDFs are available"],
        ["Submission Readiness", "GO", "README, architecture diagram, Docker files, tests, and code structure are present"],
        ["Production Readiness", "NO-GO", "Authentication, rate limiting, SSL certificate handling, and Azure AI Search are missing"],
        ["Azure Cloud Readiness", "CONDITIONAL", "Azure OpenAI is integrated; Azure AI Search and deployment templates remain future work"],
    ], [48, 35, 97])

    pdf.section("18. Capstone Evaluation Score")
    pdf.table([
        ["Category", "Score"],
        ["Business Requirements", "8 / 10"],
        ["Functional Requirements", "8 / 10"],
        ["System Architecture", "8 / 10"],
        ["Multi-Agent Architecture", "8.5 / 10"],
        ["RAG Pipeline", "7 / 10"],
        ["API Design", "7 / 10"],
        ["Frontend", "7.5 / 10"],
        ["Backend", "7.5 / 10"],
        ["Azure Integration", "5 / 10"],
        ["Security", "4.5 / 10"],
        ["Testing", "5 / 10"],
        ["Overall", "76.5 / 100 - B+"],
    ], [100, 80])

    pdf.section("19. Submission Readiness Report")
    pdf.table([
        ["Deliverable", "Status"],
        ["README", "Complete"],
        ["Streamlit UI", "Complete"],
        ["FastAPI Backend", "Complete"],
        ["LangGraph Multi-Agent Workflow", "Complete"],
        ["RAG Pipeline", "Complete with ChromaDB"],
        ["Sample Documents", "Complete"],
        ["Dockerfile", "Complete"],
        ["docker-compose.yml", "Complete"],
        ["Architecture Diagram", "Complete - architecture_diagram.png"],
        ["Tests", "Partial - API tests present"],
        ["Final Presentation Deck", "Still needed"],
        ["Azure AI Search", "Target architecture only, not implemented"],
    ], [90, 90])

    pdf.section("20. Final Justification")
    pdf.para("This capstone project is justified because it demonstrates a realistic enterprise AI solution with clear business value, working frontend and backend components, multi-agent workflow orchestration, RAG-based grounding, source citation, responsible AI checks, monitoring, Docker packaging, and sample research documents for demonstration.")
    pdf.para("The project is strong enough for capstone demonstration and submission. It should be positioned as a working proof-of-concept rather than a production-grade enterprise deployment. The most important future improvements are Azure AI Search integration, authentication, rate limiting, Key Vault secret management, persistent metrics, and stronger automated testing.")


def main():
    pdf = JustificationPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.title_page()
    add_content(pdf)
    pdf.output(str(OUTPUT_PATH))
    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
