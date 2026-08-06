"""
Generates a focused code-wise justification PDF for agents, RAG pipeline, and app.py.
Run: python data/generate_code_wise_justification_pdf.py
"""

from fpdf import FPDF, XPos, YPos
from pathlib import Path

OUTPUT_PATH = Path("Code_Wise_Justification_Report.pdf")


class CodeJustificationPDF(FPDF):
    def header(self):
        self.set_fill_color(20, 65, 105)
        self.rect(0, 0, self.w, 15, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.cell(0, 9, "Code-Wise Justification - Agents, RAG Pipeline, and Streamlit App", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(105, 105, 105)
        self.cell(0, 10, f"Page {self.page_no()} | Enterprise Business / Market Intelligence Capstone", align="C")

    def cover(self):
        self.add_page()
        self.ln(22)
        self.set_text_color(20, 65, 105)
        self.set_font("Helvetica", "B", 21)
        self.set_x(self.l_margin)
        self.multi_cell(0, 11, "Code-Wise Justification Report", align="C")
        self.set_font("Helvetica", "B", 15)
        self.set_x(self.l_margin)
        self.multi_cell(0, 9, "Agents, RAG Pipeline, and Streamlit Frontend", align="C")
        self.ln(8)
        self.set_text_color(70, 70, 70)
        self.set_font("Helvetica", "", 11)
        self.set_x(self.l_margin)
        self.multi_cell(0, 7, "Enterprise Business / Market Intelligence Multi-Agent Market Research and Executive Reporting Platform", align="C")
        self.ln(15)
        self.set_fill_color(235, 243, 250)
        self.set_draw_color(20, 65, 105)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 9, "Prepared for Capstone Technical Justification / Viva", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.cell(0, 9, "Focus Areas: Research Agent, Verifier Agent, Summarizer Agent, Report Generator Agent, RAG Pipeline, app.py", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(10)
        self.set_font("Helvetica", "", 9.5)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "This document explains the actual code implementation and justifies why each component exists, what functionality it provides, and how it supports the business and technical objectives of the capstone project.", align="C")

    def section(self, title):
        self.ln(3)
        self.set_fill_color(20, 65, 105)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def subsection(self, title):
        self.ln(2)
        self.set_text_color(20, 65, 105)
        self.set_font("Helvetica", "B", 10.5)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, title)
        self.set_text_color(0, 0, 0)

    def para(self, text):
        self.set_font("Helvetica", "", 9.4)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullets(self, items):
        self.set_font("Helvetica", "", 9.4)
        for item in items:
            self.set_x(self.l_margin)
            self.cell(5, 5.5, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_x(self.l_margin + 5)
            self.multi_cell(0, 5.5, item)
        self.ln(1)

    def code(self, text):
        self.set_fill_color(246, 248, 250)
        self.set_draw_color(210, 220, 230)
        self.set_text_color(30, 30, 30)
        self.set_font("Courier", "", 7.8)
        lines = text.strip("\n").splitlines()
        line_height = 4.4
        height = max(7, len(lines) * line_height + 3)
        if self.get_y() + height > self.page_break_trigger:
            self.add_page()
        x = self.l_margin
        y = self.get_y()
        self.rect(x, y, self.epw, height, "DF")
        self.set_xy(x + 2, y + 2)
        for line in lines:
            safe_line = line[:112]
            self.cell(0, line_height, safe_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_x(x + 2)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def table(self, rows, widths):
        self.set_font("Helvetica", "", 8.4)
        for row_index, row in enumerate(rows):
            fill = row_index == 0
            if fill:
                self.set_font("Helvetica", "B", 8.4)
                self.set_fill_color(232, 241, 250)
            else:
                self.set_font("Helvetica", "", 8.4)
                self.set_fill_color(255, 255, 255)
            x = self.get_x()
            y = self.get_y()
            line_counts = []
            for value, width in zip(row, widths):
                lines = self.multi_cell(width, 4.8, str(value), split_only=True)
                line_counts.append(max(1, len(lines)))
            row_height = max(7, max(line_counts) * 4.8)
            if y + row_height > self.page_break_trigger:
                self.add_page()
                x = self.get_x()
                y = self.get_y()
            for value, width in zip(row, widths):
                self.set_xy(x, y)
                self.multi_cell(width, 4.8, str(value), border=1, fill=fill)
                x += width
            self.set_xy(self.l_margin, y + row_height)
        self.ln(2)


def add_report_content(pdf: CodeJustificationPDF):
    pdf.add_page()
    pdf.section("1. Overall Code-Wise Justification")
    pdf.para("The project implements a complete AI engineering workflow. The frontend in app.py collects user input, the FastAPI backend exposes REST endpoints, the RAG pipeline converts uploaded documents into searchable embeddings, LangGraph orchestrates multiple agents, and each agent performs a specific business responsibility.")
    pdf.bullets([
        "Research Agent retrieves source-backed information from the vector store.",
        "Verifier Agent checks whether generated answers are grounded in source excerpts.",
        "Summarizer Agent converts raw research output into business-friendly insights.",
        "Report Generator Agent creates executive-ready reports with citations.",
        "RAG pipeline ensures responses come from uploaded documents, not unsupported model memory.",
        "app.py provides the user-facing workflow for upload, research, reporting, and monitoring.",
    ])

    pdf.section("2. Research Agent Justification")
    pdf.subsection("File: agents/research_agent.py")
    pdf.para("The Research Agent is responsible for retrieving relevant market intelligence from the vector database and generating an answer using only retrieved document context.")
    pdf.code('''def _load_vectorstore() -> Chroma:
    return Chroma(
        collection_name="market_intelligence",
        embedding_function=load_embeddings(),
        persist_directory="vectorstore",
    )''')
    pdf.para("This code connects the agent to the persistent ChromaDB vector store. The collection name groups all market intelligence document embeddings under one searchable index.")
    pdf.code('''retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})''')
    pdf.para("This retrieves the top-k most semantically relevant chunks for the user's question. It supports meaning-based document search instead of keyword-only matching.")
    pdf.code('''qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)''')
    pdf.para("RetrievalQA combines the retrieved chunks with the Azure OpenAI chat model. return_source_documents=True is critical because sources are needed later for verification and citations.")
    pdf.code('''sources = [
    {
        "content": doc.page_content[:300],
        "source": doc.metadata.get("source", "unknown"),
        "page": doc.metadata.get("page", "N/A"),
    }
    for doc in source_docs
]''')
    pdf.para("This creates a clean evidence list containing the source filename, page number, and content preview. These values are displayed in the UI and passed to the Verifier Agent.")
    pdf.subsection("Business Justification")
    pdf.para("The Research Agent ensures the solution is not a simple chatbot. It makes every answer document-grounded, which is essential for enterprise research and auditability.")

    pdf.section("3. Verifier Agent Justification")
    pdf.subsection("File: agents/verifier_agent.py")
    pdf.para("The Verifier Agent is a responsible AI control. It checks whether the Research Agent's answer is supported by the retrieved source excerpts.")
    pdf.code('''_VERIFIER_SYSTEM = """You are a strict fact-checking assistant.
- If every key claim is supported, respond with VERIFIED.
- If any claim is unsupported, respond with UNVERIFIED.
"""''')
    pdf.para("The prompt defines the agent's role as a strict fact-checker. This prevents unsupported claims from being accepted as final business insights.")
    pdf.code('''if not sources:
    return {
        **state,
        "verified": False,
        "verification_note": "No source documents available for verification.",
    }''')
    pdf.para("If no sources are retrieved, the answer cannot be trusted. The code correctly marks the response as unverified.")
    pdf.code('''verified = verdict_text.upper().startswith("VERIFIED")
return {**state, "verified": verified, "verification_note": verdict_text}''')
    pdf.para("The natural-language verifier response is converted into a Boolean workflow flag. LangGraph uses this flag to decide whether to retry research or continue.")
    pdf.subsection("Business Justification")
    pdf.para("This agent reduces hallucination risk and helps the platform meet responsible AI expectations by validating claims before summary or report generation.")

    pdf.section("4. Summarizer Agent Justification")
    pdf.subsection("File: agents/summarizer_agent.py")
    pdf.para("The Summarizer Agent converts raw retrieved insights into concise business language suitable for decision-makers.")
    pdf.code('''_SUMMARIZER_SYSTEM = """You are an expert business analyst.
Structure your response with:
- Key Findings
- Industry Trends
- Competitive Landscape
- Opportunities
- Risks
"""''')
    pdf.para("The prompt enforces a structured business summary format. This directly supports market intelligence workflows where executives need concise and categorized insights.")
    pdf.code('''if state.get("error"):
    return {
        **state,
        "summary": "Research could not be completed..."
    }''')
    pdf.para("The summarizer checks whether the previous retrieval step failed. This avoids generating misleading summaries from invalid data.")
    pdf.code('''if not raw_insights.strip() or "could not be found" in raw_insights.lower():
    return {
        **state,
        "summary": "Insufficient information found in documents...",
    }''')
    pdf.para("This guard clause enforces answer-not-found behavior and prevents unsupported summary generation.")
    pdf.subsection("Business Justification")
    pdf.para("This agent translates technical or fragmented document excerpts into executive-friendly findings, opportunities, and risks.")

    pdf.section("5. Report Generator Agent Justification")
    pdf.subsection("File: agents/report_generator_agent.py")
    pdf.para("The Report Generator Agent produces a complete executive report with standard business sections and citations.")
    pdf.code('''_REPORT_SYSTEM = """Your report must follow this structure:
## Executive Summary
## Industry Overview
## Competitor Analysis
## Market Opportunities
## Risks and Challenges
## Strategic Recommendations
## Citations and References
"""''')
    pdf.para("The system prompt forces the model to generate a consistent executive report structure. This makes the output suitable for leadership review and presentation.")
    pdf.code('''def _format_sources(sources: list[dict]) -> str:
    return "\n".join(
        f"[{i+1}] Source: {s.get('source')}, Page: {s.get('page')}"
        for i, s in enumerate(sources)
    )''')
    pdf.para("Source formatting gives the LLM numbered references before report generation, improving citation discipline.")
    pdf.code('''def _extract_citations(sources: list[dict]) -> list[str]:
    return [
        f"[{i+1}] {s.get('source', 'unknown')} - Page {s.get('page', 'N/A')}"
        for i, s in enumerate(sources)
    ]''')
    pdf.para("Citation extraction creates a separate citation list for the UI. This makes sources visible and auditable.")
    pdf.code('''if not summary.strip():
    return {
        **state,
        "report": "Unable to generate report: no summarized insights available.",
        "citations": [],
    }''')
    pdf.para("This prevents the system from producing a fabricated executive report when no validated summary exists.")
    pdf.subsection("Business Justification")
    pdf.para("This agent transforms research into a professional deliverable: an executive-ready report with recommendations, risks, and citations.")

    pdf.section("6. LangGraph Workflow Justification")
    pdf.subsection("File: workflows/langgraph_workflow.py")
    pdf.para("LangGraph connects all agents into a controlled multi-step workflow. This proves the project uses agentic AI orchestration rather than one disconnected LLM call.")
    pdf.code('''graph.add_node("research", run_research_agent)
graph.add_node("verifier", run_verifier_agent)
graph.add_node("summarizer", run_summarizer_agent)
graph.add_node("report_generator", run_report_generator_agent)''')
    pdf.para("Each business function is implemented as a separate graph node. This improves modularity, explainability, and testing.")
    pdf.code('''graph.add_conditional_edges(
    "verifier",
    _route_after_verification,
    {"research": "increment_retry", "summarizer": "summarizer"},
)''')
    pdf.para("This conditional edge adds verification-based routing. If the answer is not verified, the system retries research once before continuing.")
    pdf.code('''if not verified and retry_count < 1:
    return "research"
return "summarizer"''')
    pdf.para("The retry limit avoids infinite loops while still improving answer quality. This is a strong responsible AI design decision.")

    pdf.section("7. RAG Pipeline Justification")
    pdf.subsection("File: vectorstore/ingest.py")
    pdf.para("The RAG pipeline prepares documents for semantic retrieval. It is responsible for loading files, splitting text, generating embeddings, and storing vectors.")
    pdf.code('''SUPPORTED_SUFFIXES = {".pdf", ".docx", ".txt"}''')
    pdf.para("The system supports standard business document formats used in market intelligence work.")
    pdf.code('''if path.suffix.lower() == ".pdf":
    loader = PyPDFLoader(str(path))
elif path.suffix.lower() == ".docx":
    loader = Docx2txtLoader(str(path))
else:
    loader = TextLoader(str(path), encoding="utf-8")''')
    pdf.para("Each file type uses the correct document loader. This makes the ingestion pipeline flexible and reusable.")
    pdf.code('''for doc in loaded:
    doc.metadata["source"] = path.name''')
    pdf.para("Source metadata is preserved on every document object. This metadata later appears in citations.")
    pdf.code('''splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)''')
    pdf.para("Documents are split into 800-character chunks with 100-character overlap. This prevents long documents from exceeding LLM context limits and preserves meaning across chunk boundaries.")
    pdf.code('''vectorstore = get_vectorstore()
vectorstore._collection.delete(where={"source": source_name})''')
    pdf.para("When a single file is uploaded again, old chunks for that file are deleted. This prevents duplicate results in retrieval.")
    pdf.code('''embeddings = embed_texts(texts)
vectorstore._collection.upsert(
    ids=ids,
    documents=texts,
    metadatas=metadatas,
    embeddings=embeddings,
)''')
    pdf.para("Text chunks are converted into Azure OpenAI embeddings and saved into ChromaDB with metadata. This enables semantic search during user queries.")
    pdf.subsection("Business Justification")
    pdf.para("The RAG pipeline makes the project enterprise-ready at the concept level because answers are grounded in approved documents instead of public internet content or model memory.")

    pdf.section("8. Streamlit app.py Justification")
    pdf.subsection("File: frontend/app.py")
    pdf.para("app.py is the user-facing business dashboard. It allows users to upload documents, ask research questions, generate executive reports, and monitor platform usage.")
    pdf.code('''API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")''')
    pdf.para("This allows the UI to call the backend locally or inside Docker by changing only an environment variable.")
    pdf.code('''st.set_page_config(
    page_title="Market Intelligence Platform",
    page_icon="MI",
    layout="wide",
    initial_sidebar_state="expanded",
)''')
    pdf.para("The app is configured as a wide dashboard, suitable for research output, source review, monitoring, and reporting.")
    pdf.code('''page = st.sidebar.radio(
    "Navigate to",
    ["Home", "Research Dashboard", "Executive Report", "Monitoring Dashboard"],
)''')
    pdf.para("The UI is separated into four business workflows: upload/query, research analysis, report generation, and monitoring.")
    pdf.code('''health = requests.get(f"{API_BASE}/health", timeout=5).json()
st.sidebar.success(f"API online - v{health.get('version', '?')}")''')
    pdf.para("The sidebar performs a live backend health check, helping users know whether the FastAPI service is available.")
    pdf.code('''uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, or TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)''')
    pdf.para("The Home page lets users upload multiple research documents in common business formats.")
    pdf.code('''resp = requests.post(f"{API_BASE}/upload-document", files=files, timeout=180)''')
    pdf.para("Uploaded documents are sent to the backend, where they are saved and indexed into the vectorstore.")
    pdf.code('''resp = requests.post(
    f"{API_BASE}/research",
    json={"query": query, "top_k": 5},
    timeout=600,
)''')
    pdf.para("The frontend sends user research questions to the backend. The top_k value controls how many relevant chunks the Research Agent retrieves.")
    pdf.code('''def _report_to_pdf(report_text: str, title: str = "Executive Report") -> bytes:''')
    pdf.para("The app converts generated reports into downloadable PDF files, making the output usable for capstone submission and executive presentation.")
    pdf.subsection("Business Justification")
    pdf.para("The Streamlit app turns the technical AI backend into an accessible business product. Users do not need to understand LangGraph, embeddings, or APIs to use the system.")

    pdf.section("9. End-to-End Code Flow")
    pdf.code('''User uploads PDF in app.py
    -> POST /upload-document
    -> backend/main.py saves file
    -> vectorstore/ingest.py chunks and embeds document
    -> ChromaDB stores vectors
    -> User asks query in app.py
    -> POST /research
    -> LangGraph starts workflow
    -> Research Agent retrieves chunks
    -> Verifier Agent checks grounding
    -> Summarizer Agent prepares business summary
    -> Streamlit displays insights, sources, and verification status''')
    pdf.para("This flow proves the platform is an integrated AI application, not a collection of isolated scripts.")

    pdf.section("10. Final Code-Wise Defense Statement")
    pdf.para("The project is justified code-wise because each module has a clear responsibility and contributes directly to the business objective. The agents implement the intelligence layer, the RAG pipeline implements document grounding, LangGraph implements controlled orchestration, and app.py implements the user-facing business workflow.")
    pdf.para("The strongest defense point is: this is not a simple chatbot. It is a multi-agent, RAG-based, source-grounded executive reporting platform with retrieval, verification, summarization, citations, monitoring, and PDF report generation.")

    pdf.section("11. Quick Viva Answers")
    pdf.table([
        ["Question", "Answer"],
        ["Why use RAG?", "To make answers come from uploaded business documents instead of unsupported model memory."],
        ["Why use multiple agents?", "Each agent has one responsibility: retrieve, verify, summarize, or report."],
        ["Why use Verifier Agent?", "To reduce hallucination and check whether claims are supported by sources."],
        ["Why use LangGraph?", "To orchestrate the agents and implement conditional retry logic."],
        ["Why use ChromaDB?", "It stores document embeddings and enables semantic similarity search."],
        ["Why use Streamlit?", "It quickly provides a business-friendly interface for upload, research, reports, and monitoring."],
        ["Why use FastAPI?", "It provides clean REST endpoints, validation, and Swagger documentation."],
    ], [55, 125])


def main():
    pdf = CodeJustificationPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.cover()
    add_report_content(pdf)
    pdf.output(str(OUTPUT_PATH))
    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
