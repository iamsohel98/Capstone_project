"""
Generates two sample research PDFs for testing the Market Intelligence platform.
Run:  python data/generate_sample_pdfs.py
"""

from fpdf import FPDF, XPos, YPos
import os

OUTPUT_DIR = "data/sample_documents"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class ResearchPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(30, 80, 160)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "  MARKET INTELLIGENCE RESEARCH REPORT",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10,
                  "Page " + str(self.page_no()) + " | Confidential - Sample Document Only",
                  align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_fill_color(230, 240, 255)
        self.set_text_color(20, 60, 140)
        self.cell(0, 9, "  " + title,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, items):
        self.set_font("Helvetica", "", 10)
        for item in items:
            self.set_x(self.l_margin)
            self.cell(8, 6, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.multi_cell(0, 6, item)
        self.ln(2)

    def key_stat(self, label, value):
        self.set_font("Helvetica", "B", 10)
        self.cell(75, 7, label + ":", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 7, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def create_genai_report():
    pdf = ResearchPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 60, 140)
    pdf.multi_cell(0, 10, "Generative AI Enterprise Adoption\nResearch Report 2024", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 7, "Prepared by: Market Intelligence Research Division | July 2024",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    pdf.chapter_title("Key Statistics at a Glance")
    pdf.key_stat("Global GenAI Market Size (2023)", "$44 Billion")
    pdf.key_stat("Projected Market Size (2030)", "$667 Billion")
    pdf.key_stat("CAGR (2023-2030)", "42%")
    pdf.key_stat("Fortune 500 Companies with GenAI Pilots", "65%")
    pdf.key_stat("AI Inference Cost Reduction (2022-2024)", "90%")
    pdf.key_stat("North America Market Share", "38%")
    pdf.key_stat("Asia-Pacific Market Share", "28%")
    pdf.key_stat("Europe Market Share", "22%")
    pdf.ln(4)

    pdf.chapter_title("1. Executive Summary")
    pdf.body_text(
        "The Generative AI market is experiencing unprecedented growth, driven by enterprise adoption "
        "across financial services, healthcare, manufacturing, and retail sectors. As of 2023, the "
        "market is valued at approximately $44 billion and is projected to reach $667 billion by 2030, "
        "growing at a CAGR of 42%. Over 65% of Fortune 500 companies have deployed at least one "
        "Generative AI pilot project. AI inference costs dropped by 90% between 2022 and 2024, "
        "dramatically accelerating adoption across all industry sectors."
    )

    pdf.chapter_title("2. Market Size and Regional Analysis")
    pdf.body_text(
        "North America leads global GenAI adoption with a 38% market share, driven primarily by "
        "hyperscaler investments from Microsoft, Google, Amazon, and Meta. The United States alone "
        "accounts for 31% of global GenAI enterprise spending."
    )
    pdf.body_text(
        "Asia-Pacific represents 28% of the market, with strong growth in Japan, South Korea, "
        "Singapore, and India. The region is expected to surpass Europe by 2026."
    )
    pdf.body_text(
        "Europe holds 22% market share, with the EU AI Act expected to reshape compliance "
        "requirements. Regulated industries face the highest compliance costs, estimated at "
        "15-20% of total AI deployment budgets."
    )

    pdf.chapter_title("3. Key Industry Trends")
    pdf.section_title("3.1 Retrieval-Augmented Generation (RAG)")
    pdf.body_text(
        "RAG has emerged as the dominant architecture for enterprise knowledge management. "
        "By combining vector search with large language model generation, enterprises can ground "
        "AI outputs in verified internal documents. Adoption of RAG grew from 12% in 2022 to "
        "58% of enterprise AI projects in 2024."
    )
    pdf.section_title("3.2 Multi-Agent AI Systems")
    pdf.body_text(
        "Multi-agent AI architectures are gaining rapid traction for complex business workflows. "
        "LangGraph, AutoGen, and CrewAI are the leading frameworks. Enterprise use cases include "
        "automated report generation, multi-step research workflows, and compliance review pipelines. "
        "45% of new enterprise AI projects in 2024 incorporate at least two AI agents."
    )
    pdf.section_title("3.3 Cost Reduction Trends")
    pdf.body_text(
        "The cost of running AI inference dropped by 90% between 2022 and 2024, driven by GPU "
        "price reductions, model quantization, and competition between cloud providers. "
        "GPT-4 class model API costs dropped from $0.06 per 1K tokens in 2023 to $0.002 per "
        "1K tokens by mid-2024 across competing providers."
    )
    pdf.section_title("3.4 Responsible AI and Governance")
    pdf.body_text(
        "Enterprise AI governance frameworks are maturing rapidly. 78% of large enterprises now "
        "have a formal AI policy. Key controls include hallucination detection, citation requirements, "
        "human review for high-risk outputs, and audit logging. The EU AI Act enforcement timeline "
        "(2025-2026) is accelerating governance investment across all regulated sectors."
    )

    pdf.add_page()
    pdf.chapter_title("4. Market Opportunities")
    pdf.bullet([
        "Healthcare AI: Clinical decision support represents a $45B opportunity by 2028.",
        "Financial Services: Automated report generation showing 30-40% cost savings.",
        "Customer Service: AI agents reducing service costs by 30-40% in pilot deployments.",
        "Supply Chain: Predictive analytics showing 15-20% efficiency gains in logistics.",
        "Legal and Compliance: Contract analysis saving 60% of manual review time.",
        "Human Resources: AI-driven talent matching reducing hiring time by 35%.",
    ])

    pdf.chapter_title("5. Risks and Challenges")
    pdf.bullet([
        "Hallucination Rates: 23% of enterprise deployments report accuracy issues.",
        "Data Privacy: Sovereignty requirements vary significantly by region.",
        "Talent Shortage: 67% of companies cite lack of AI engineering talent as top barrier.",
        "Model Dependency Risk: Over-reliance on a single LLM provider creates supply chain risk.",
        "Regulatory Uncertainty: EU AI Act enforcement creates cost and timeline uncertainty.",
        "Security: Prompt injection attacks identified in 18% of enterprise AI applications.",
        "Integration Complexity: Legacy system integration cited as top challenge by 54% of IT leaders.",
    ])

    pdf.chapter_title("6. Strategic Recommendations")
    recommendations = [
        "Implement RAG architecture for all document-heavy knowledge management use cases.",
        "Establish a multi-provider LLM strategy to reduce vendor lock-in and cost exposure.",
        "Deploy human-in-the-loop review for all high-stakes AI outputs (financial, medical, legal).",
        "Invest in LLMOps and prompt engineering capabilities before scaling deployments.",
        "Align AI governance with EU AI Act requirements - global standards are converging.",
        "Prioritise healthcare and financial services use cases for highest near-term ROI.",
    ]
    for i, rec in enumerate(recommendations, 1):
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(12, 6, str(i) + ".", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, rec)
    pdf.ln(2)

    pdf.chapter_title("7. Sources and References")
    pdf.bullet([
        "McKinsey Global Institute: The Economic Potential of Generative AI (2024)",
        "Gartner Hype Cycle for Artificial Intelligence (2024)",
        "IDC Worldwide AI Spending Guide - Semiannual Update (2024)",
        "Bloomberg Intelligence: Generative AI Forecast (2024)",
        "Stanford HAI: AI Index Report 2024",
        "Forrester: Enterprise AI Adoption Survey (Q1 2024)",
        "PwC Global AI Study: Exploiting the AI Revolution (2024)",
    ])

    path = os.path.join(OUTPUT_DIR, "GenAI_Enterprise_Adoption_Report_2024.pdf")
    pdf.output(path)
    print("Created: " + path)


def create_competitor_report():
    pdf = ResearchPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 60, 140)
    pdf.multi_cell(0, 10, "Enterprise AI Platform\nCompetitor Analysis Report 2024", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 7, "Prepared by: Competitive Intelligence Unit | Q2 2024",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    pdf.chapter_title("Market Share Overview (Enterprise AI Platforms, 2024)")
    shares = [
        ("Microsoft Azure AI", "34%", "#1"),
        ("Google Cloud AI", "23%", "#2"),
        ("Amazon Web Services AI", "21%", "#3"),
        ("IBM watsonx", "8%", "#4"),
        ("Others (Salesforce, Oracle, SAP)", "14%", "#5+"),
    ]
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(80, 7, "Vendor", border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(45, 7, "Market Share", border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(30, 7, "Rank", border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    for vendor, share, rank in shares:
        pdf.cell(80, 7, vendor, border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(45, 7, share, border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(30, 7, rank, border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.chapter_title("Company A: Microsoft Azure AI")
    pdf.key_stat("Market Position", "#1 in enterprise AI cloud services (IDC, 2024)")
    pdf.key_stat("AI Services Revenue (2023)", "$8.7 Billion")
    pdf.key_stat("Innovation Score (Gartner 2024)", "8.7 / 10")
    pdf.key_stat("Customer Satisfaction NPS", "52")
    pdf.key_stat("Compliance Certifications", "100+")
    pdf.key_stat("Partner Network", "400,000+ resellers and system integrators")
    pdf.ln(2)
    pdf.section_title("Key Products")
    pdf.bullet([
        "Azure OpenAI Service - Enterprise deployment of GPT-4o",
        "Microsoft Copilot for Microsoft 365 - Integrated workplace AI",
        "Azure Machine Learning - End-to-end MLOps platform",
        "GitHub Copilot - AI-assisted software development",
    ])
    pdf.section_title("Strengths")
    pdf.bullet([
        "Deep enterprise integration with Microsoft 365 and Teams ecosystem",
        "Regulatory compliance certifications across 100+ standards",
        "Exclusive enterprise access to OpenAI GPT-4o via Azure",
        "Strong brand trust in regulated industries (banking, healthcare, government)",
    ])
    pdf.section_title("Weaknesses")
    pdf.bullet([
        "Higher pricing compared to open-source alternatives",
        "Complex licensing and consumption-based pricing model",
        "Slower pure research output compared to Google DeepMind",
    ])

    pdf.add_page()
    pdf.chapter_title("Company B: Google Cloud AI")
    pdf.key_stat("Market Position", "#2 in enterprise AI platform market")
    pdf.key_stat("AI Services Revenue (2023)", "$6.1 Billion")
    pdf.key_stat("Innovation Score (Gartner 2024)", "8.9 / 10")
    pdf.key_stat("Customer Satisfaction NPS", "44")
    pdf.key_stat("Primary LLM", "Gemini 1.5 Pro (multimodal)")
    pdf.ln(2)
    pdf.section_title("Key Products")
    pdf.bullet([
        "Vertex AI - Managed ML and LLM platform",
        "Gemini Enterprise - Multimodal AI for business",
        "Google Workspace AI - Integrated productivity AI",
        "BigQuery ML - In-database machine learning",
    ])
    pdf.section_title("Strengths")
    pdf.bullet([
        "Leading AI research capability through Google DeepMind",
        "Best-in-class multimodal AI (text, image, video, audio)",
        "Strong open-source contributions - TensorFlow, JAX, Gemma",
        "Competitive pricing with sustained use discounts",
    ])
    pdf.section_title("Weaknesses")
    pdf.bullet([
        "Smaller enterprise sales force compared to Microsoft",
        "Lower brand trust in highly regulated industries",
        "History of product discontinuations reducing enterprise confidence",
    ])

    pdf.chapter_title("Company C: Amazon Web Services AI")
    pdf.key_stat("Market Position", "#3 in enterprise AI services by revenue")
    pdf.key_stat("AI Services Revenue (2023)", "$5.4 Billion")
    pdf.key_stat("Innovation Score (Gartner 2024)", "7.9 / 10")
    pdf.key_stat("Customer Satisfaction NPS", "48")
    pdf.key_stat("LLM Platform", "Amazon Bedrock - 20+ models")
    pdf.ln(2)
    pdf.section_title("Key Products")
    pdf.bullet([
        "Amazon Bedrock - Multi-model LLM API platform",
        "Amazon SageMaker - End-to-end ML lifecycle management",
        "Amazon Q Business - Enterprise AI assistant",
        "AWS Trainium / Inferentia - Custom AI chips",
    ])
    pdf.section_title("Strengths")
    pdf.bullet([
        "Multi-model flexibility via Bedrock (Anthropic, Meta, Mistral and others)",
        "Largest global cloud infrastructure footprint",
        "Strong data lake integration with S3, Redshift, Athena",
        "Cost-effective training with proprietary AWS Trainium chips",
    ])
    pdf.section_title("Weaknesses")
    pdf.bullet([
        "Less mature agentic AI capabilities versus Microsoft",
        "Developer tooling and user experience rated below competitors",
        "Slower enterprise AI product innovation release cycle",
    ])

    pdf.add_page()
    pdf.chapter_title("Strategic Comparison Matrix")
    criteria = [
        "Enterprise Ecosystem",
        "AI Research",
        "Pricing",
        "Compliance",
        "Developer Experience",
    ]
    scores = {
        "Microsoft": [5, 4, 3, 5, 4],
        "Google": [4, 5, 4, 3, 4],
        "AWS": [4, 3, 5, 4, 3],
    }
    stars = {1: "*", 2: "**", 3: "***", 4: "****", 5: "*****"}
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(65, 7, "Criteria", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    for vendor in scores:
        pdf.cell(40, 7, vendor, border=1, align="C",
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    for i, criterion in enumerate(criteria):
        pdf.cell(65, 7, criterion, border=1,
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        for vendor in scores:
            pdf.cell(40, 7, stars[scores[vendor][i]], border=1, align="C",
                     new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.ln()
    pdf.ln(4)

    pdf.chapter_title("Conclusions and Recommendations")
    pdf.body_text(
        "Microsoft maintains enterprise AI market leadership through deep ecosystem integration "
        "and unmatched compliance certifications. For organisations already invested in "
        "Microsoft 365, Azure AI provides the lowest integration friction and highest compliance assurance."
    )
    pdf.body_text(
        "Google leads on pure AI research and multimodal capabilities. Organisations requiring "
        "cutting-edge vision, audio, or code generation should evaluate Vertex AI and Gemini 1.5 Pro."
    )
    pdf.body_text(
        "AWS provides the most cost-effective multi-model flexibility for cloud-native organisations. "
        "Amazon Bedrock reduces vendor lock-in risk by supporting models from Anthropic, Meta, and Mistral."
    )
    pdf.body_text(
        "Recommendation: Base vendor selection on existing cloud footprint and compliance requirements. "
        "A dual-provider strategy (Microsoft + AWS or Microsoft + Google) is advised for large enterprises "
        "to balance cost, capability, and risk."
    )

    pdf.chapter_title("Sources")
    pdf.bullet([
        "IDC MarketScape: Worldwide General-Purpose AI Services 2024 Vendor Assessment",
        "Gartner Magic Quadrant for Cloud AI Developer Services (2024)",
        "Forrester Wave: AI Infrastructure Platforms, Q1 2024",
        "Company Annual Reports: Microsoft FY2024, Alphabet Q4 2023, Amazon FY2023",
        "Bloomberg Second Measure: Enterprise Cloud AI Spending Survey (2024)",
    ])

    path = os.path.join(OUTPUT_DIR, "Enterprise_AI_Competitor_Analysis_2024.pdf")
    pdf.output(path)
    print("Created: " + path)


if __name__ == "__main__":
    create_genai_report()
    create_competitor_report()
    print("\nBoth PDFs ready in data/sample_documents/")
    print("Next step: python vectorstore/ingest.py")
