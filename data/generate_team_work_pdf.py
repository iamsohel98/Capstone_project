"""
Generates a PDF for team work distribution and demo speaking responsibilities.
Run: python data/generate_team_work_pdf.py
"""

from fpdf import FPDF, XPos, YPos
from pathlib import Path

OUTPUT_PATH = Path("Team_Work_Distribution_Report.pdf")


class TeamWorkPDF(FPDF):
    def header(self):
        self.set_fill_color(24, 75, 125)
        self.rect(0, 0, self.w, 15, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.cell(0, 9, "Team Work Distribution - Market Intelligence Capstone", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(105, 105, 105)
        self.cell(0, 10, f"Page {self.page_no()} | Group 5 Capstone Project", align="C")

    def cover(self):
        self.add_page()
        self.ln(22)
        self.set_text_color(24, 75, 125)
        self.set_font("Helvetica", "B", 21)
        self.set_x(self.l_margin)
        self.multi_cell(0, 11, "Team Work Distribution Report", align="C")
        self.set_font("Helvetica", "B", 15)
        self.set_x(self.l_margin)
        self.multi_cell(0, 9, "Enterprise Business / Market Intelligence", align="C")
        self.ln(6)
        self.set_text_color(70, 70, 70)
        self.set_font("Helvetica", "", 11)
        self.set_x(self.l_margin)
        self.multi_cell(0, 7, "Multi-Agent Market Research and Executive Reporting Platform", align="C")
        self.ln(14)
        self.set_fill_color(235, 243, 250)
        self.set_draw_color(24, 75, 125)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 9, "Purpose: Assign clear demo responsibilities to every team member", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.cell(0, 9, "Use Case: Teams recording, viva preparation, and capstone submission", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(10)
        self.set_font("Helvetica", "", 9.5)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "This document divides project responsibilities across six team members and provides simple speaking points so every person can explain their contribution clearly during the final demo recording.", align="C")

    def section(self, title):
        self.ln(3)
        self.set_fill_color(24, 75, 125)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def subsection(self, title):
        self.ln(2)
        self.set_text_color(24, 75, 125)
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

    def table(self, rows, widths):
        for row_index, row in enumerate(rows):
            fill = row_index == 0
            if fill:
                self.set_font("Helvetica", "B", 8.2)
                self.set_fill_color(232, 241, 250)
            else:
                self.set_font("Helvetica", "", 8.2)
                self.set_fill_color(255, 255, 255)
            x = self.get_x()
            y = self.get_y()
            line_counts = []
            for value, width in zip(row, widths):
                lines = self.multi_cell(width, 4.7, str(value), split_only=True)
                line_counts.append(max(1, len(lines)))
            row_height = max(7, max(line_counts) * 4.7)
            if y + row_height > self.page_break_trigger:
                self.add_page()
                x = self.get_x()
                y = self.get_y()
            for value, width in zip(row, widths):
                self.set_xy(x, y)
                self.multi_cell(width, 4.7, str(value), border=1, fill=fill)
                x += width
            self.set_xy(self.l_margin, y + row_height)
        self.ln(2)


def add_content(pdf: TeamWorkPDF):
    pdf.add_page()
    pdf.section("1. Recommended Team Work Distribution")
    pdf.table([
        ["Team Member", "Best Work Area", "Difficulty", "Why It Is Good"],
        ["Person 1", "Streamlit UI + Business Workflow", "Easy", "Visual, easy to demonstrate, and directly connected to business value."],
        ["Person 2", "FastAPI Backend APIs", "Medium", "Clear endpoints, request flow, validation, and backend role."],
        ["Person 3", "RAG Pipeline + Documents", "Medium", "Important AI concept: document loading, chunking, embeddings, retrieval, and citations."],
        ["Person 4", "Multi-Agent Workflow", "Medium-Hard", "Strong technical contribution using LangGraph and four specialized agents."],
        ["Person 5", "Azure + Docker + Architecture", "Medium", "Good for deployment, Azure services, Docker, and architecture explanation."],
        ["Person 6", "QA + Monitoring + Documentation", "Easy-Medium", "Good for tests, metrics, logs, README, demo readiness, and final submission."],
    ], [32, 55, 28, 65])

    pdf.section("2. Person 1 - Streamlit UI + Business Workflow")
    pdf.para("This is the easiest and safest section for a team member who wants a visual, business-focused demo part.")
    pdf.subsection("What to explain")
    pdf.bullets([
        "Home page and document upload workflow.",
        "Research Dashboard and verified source-backed insights.",
        "Executive Report page and report download.",
        "Monitoring Dashboard with query count, latency, errors, token usage concept, and logs.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was the Streamlit frontend and business workflow, including document upload, research query, executive report generation, and monitoring dashboard.")
    pdf.subsection("Files to show")
    pdf.bullets(["frontend/app.py"])

    pdf.section("3. Person 2 - FastAPI Backend")
    pdf.subsection("What to explain")
    pdf.bullets([
        "FastAPI backend server.",
        "Pydantic request and response models.",
        "Health, research, report generation, upload, metrics, and logs endpoints.",
        "Request ID, latency tracking, error handling, and API documentation.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was the FastAPI backend, including API endpoints, request/response models, upload handling, metrics, logs, and error handling.")
    pdf.subsection("Files to show")
    pdf.bullets(["backend/main.py", "backend/metrics.py", "http://localhost:8000/docs"])

    pdf.section("4. Person 3 - RAG Pipeline + Documents")
    pdf.subsection("What to explain")
    pdf.bullets([
        "PDF, DOCX, and TXT document loading.",
        "Text chunking with overlap.",
        "Azure OpenAI embeddings.",
        "ChromaDB vector storage.",
        "Source metadata preservation for citations.",
        "Semantic retrieval from uploaded documents.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was the RAG pipeline, including document loading, chunking, embeddings, vector storage, and source metadata for citations.")
    pdf.subsection("Files to show")
    pdf.bullets(["vectorstore/ingest.py", "data/sample_documents/"])
    pdf.subsection("Command to show")
    pdf.para("python vectorstore/ingest.py")

    pdf.section("5. Person 4 - Multi-Agent Workflow")
    pdf.subsection("What to explain")
    pdf.bullets([
        "Research Agent retrieves source-backed insights.",
        "Verifier Agent checks grounding and hallucination risk.",
        "Summarizer Agent converts raw output into business insights.",
        "Report Generator Agent creates executive reports with citations.",
        "LangGraph orchestrates the agent flow.",
        "Conditional retry happens when verification fails.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was the LangGraph multi-agent workflow and agent logic for research, verification, summarization, and report generation.")
    pdf.subsection("Files to show")
    pdf.bullets([
        "workflows/langgraph_workflow.py",
        "agents/research_agent.py",
        "agents/verifier_agent.py",
        "agents/summarizer_agent.py",
        "agents/report_generator_agent.py",
    ])

    pdf.section("6. Person 5 - Azure + Docker + Architecture")
    pdf.subsection("What to explain")
    pdf.bullets([
        "Azure OpenAI for chat and embeddings.",
        "Dockerfile and docker-compose for container packaging.",
        "Azure Container Apps deployment plan.",
        "Azure Container Registry for image storage.",
        "Azure Key Vault and Azure Monitor as production recommendations.",
        "Azure AI Search as production vector search target.",
        "architecture_diagram.png and layered system design.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was architecture and deployment design, including Docker, Azure OpenAI integration, Azure Container Apps plan, and architecture diagram.")
    pdf.subsection("Files to show")
    pdf.bullets(["Dockerfile", "docker-compose.yml", "architecture_diagram.png", "Azure_Deployment_Checklist.md"])
    pdf.subsection("Important honest point")
    pdf.para("In the current demo, ChromaDB is used locally. For Azure production deployment, Azure AI Search is the recommended replacement for enterprise vector search.")

    pdf.section("7. Person 6 - QA + Monitoring + Documentation")
    pdf.subsection("What to explain")
    pdf.bullets([
        "API tests using pytest and FastAPI TestClient.",
        "Monitoring dashboard metrics and logs.",
        "README documentation.",
        "Demo recording script.",
        "Project justification PDFs.",
        "Final submission readiness.",
    ])
    pdf.subsection("Demo line")
    pdf.para("My contribution was QA, monitoring, and documentation, including test cases, README, demo script, justification reports, and final submission readiness.")
    pdf.subsection("Files to show")
    pdf.bullets([
        "tests/test_api.py",
        "README.md",
        "Capstone_Demo_Recording_Script.md",
        "Project_Justification_Report.pdf",
        "Code_Wise_Justification_Report.pdf",
    ])
    pdf.subsection("Command to show")
    pdf.para("python -m pytest tests/test_api.py -q")
    pdf.para("Expected output: 9 passed")

    pdf.section("8. Suggested Speaking Order")
    pdf.table([
        ["Order", "Speaker", "Topic"],
        ["1", "Person 5", "Architecture + Azure overview"],
        ["2", "Person 1", "Streamlit frontend walkthrough"],
        ["3", "Person 2", "FastAPI backend APIs"],
        ["4", "Person 3", "RAG pipeline"],
        ["5", "Person 4", "Multi-agent workflow"],
        ["6", "Person 6", "QA, monitoring, documentation, challenges"],
        ["7", "All / Team Lead", "End-to-end demo and conclusion"],
    ], [25, 45, 110])

    pdf.section("9. Short Contribution Lines")
    pdf.bullets([
        "Person 1: My contribution was the Streamlit frontend and business workflow, including document upload, research query, executive report generation, and monitoring dashboard.",
        "Person 2: My contribution was the FastAPI backend, including API endpoints, request/response models, upload handling, metrics, logs, and error handling.",
        "Person 3: My contribution was the RAG pipeline, including document loading, chunking, embeddings, vector storage, and source metadata for citations.",
        "Person 4: My contribution was the LangGraph multi-agent workflow and agent logic for research, verification, summarization, and report generation.",
        "Person 5: My contribution was architecture and deployment design, including Docker, Azure OpenAI integration, Azure Container Apps plan, and architecture diagram.",
        "Person 6: My contribution was QA, monitoring, and documentation, including test cases, README, demo script, justification reports, and final submission readiness.",
    ])

    pdf.section("10. Final Recommendation")
    pdf.para("Assign easier and more visual sections to members who are less comfortable with deep technical explanation. Assign RAG, LangGraph, Azure, and Docker to technically stronger members. This makes the Teams recording smoother and helps every person explain their part confidently.")
    pdf.bullets([
        "Easy sections: Streamlit UI, QA/documentation, demo walkthrough.",
        "Medium sections: FastAPI backend, RAG pipeline, Azure/Docker architecture.",
        "Harder section: LangGraph multi-agent workflow and verification retry logic.",
    ])


def main():
    pdf = TeamWorkPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.cover()
    add_content(pdf)
    pdf.output(str(OUTPUT_PATH))
    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
