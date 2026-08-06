"""
Streamlit Frontend — Multi-Agent Market Research & Executive Reporting Platform
"""

import io
import os
import re
import textwrap
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _report_to_pdf(report_text: str, title: str = "Executive Report") -> bytes:
    page_width = 612
    page_height = 792
    margin = 54
    top_y = page_height - 96
    bottom_y = 82
    generated_on = datetime.now().strftime("%d %b %Y")

    def clean(value: str) -> str:
        return re.sub(r"\s+", " ", value.replace("`", "")).strip()

    def is_heading(value: str) -> bool:
        plain = clean(re.sub(r"^[#>\s]+", "", value).strip("*_ "))
        if not plain:
            return False
        if value.lstrip().startswith("#"):
            return True
        if re.fullmatch(r"\*\*[^*]+\*\*", value.strip()):
            return True
        return len(plain) <= 72 and (plain.endswith(":") or plain.upper() == plain)

    def wrap_text(value: str, width: int, prefix: str = "") -> list[str]:
        wrapped = textwrap.wrap(value, width=width, break_long_words=False) or [""]
        if not prefix:
            return wrapped
        return [prefix + wrapped[0], *["  " + item for item in wrapped[1:]]]

    rows: list[dict[str, object]] = [
        {"text": title, "style": "title", "indent": 0},
        {"text": "", "style": "space", "indent": 0},
    ]

    for raw_line in (report_text or "No report generated.").splitlines():
        line = raw_line.strip()
        if not line:
            rows.append({"text": "", "style": "space", "indent": 0})
            continue

        if is_heading(line):
            heading = clean(re.sub(r"^[#>\s]+", "", line).strip("*_ :"))
            for wrapped in wrap_text(heading, 62):
                rows.append({"text": wrapped, "style": "heading", "indent": 0})
            continue

        numbered = re.match(r"^(\d+[.)])\s+(.+)$", line)
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        if numbered:
            prefix = f"{numbered.group(1)} "
            for wrapped in wrap_text(clean(numbered.group(2)), 82, prefix):
                rows.append({"text": wrapped, "style": "body", "indent": 14})
        elif bullet:
            for wrapped in wrap_text(clean(bullet.group(1)), 82, "- "):
                rows.append({"text": wrapped, "style": "body", "indent": 14})
        else:
            for wrapped in wrap_text(clean(line.strip("*_")), 90):
                rows.append({"text": wrapped, "style": "body", "indent": 0})

    def row_height(row: dict[str, object]) -> int:
        style = str(row["style"])
        if style == "title":
            return 26
        if style == "heading":
            return 22
        if style == "space":
            return 10
        return 15

    pages: list[list[dict[str, object]]] = [[]]
    y = top_y
    for row in rows:
        height = row_height(row)
        if y - height < bottom_y and pages[-1]:
            pages.append([])
            y = top_y
        pages[-1].append(row)
        y -= height

    objects: list[str] = ["<< /Type /Catalog /Pages 2 0 R >>"]
    page_ids: list[int] = []

    objects.append("<< /Type /Pages /Kids [] /Count 0 >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    font_id = 3
    bold_font_id = 4

    for page_number, page_rows in enumerate(pages, start=1):
        page_id = len(objects) + 1
        content_id = page_id + 1
        page_ids.append(page_id)
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 {font_id} 0 R /F2 {bold_font_id} 0 R >> >> /Contents {content_id} 0 R >>"
        )

        commands = [
            "0.10 0.20 0.30 rg",
            f"BT /F2 13 Tf 1 0 0 1 {margin} {page_height - 48} Tm (Market Intelligence Platform) Tj ET",
            "0.35 0.45 0.55 rg",
            f"BT /F1 9 Tf 1 0 0 1 {page_width - 178} {page_height - 48} Tm (Generated {generated_on}) Tj ET",
            "0.70 0.78 0.84 RG",
            f"{margin} {page_height - 62} m {page_width - margin} {page_height - 62} l S",
        ]

        y = top_y
        for row in page_rows:
            text = str(row["text"])
            style = str(row["style"])
            x = margin + int(row["indent"])

            if style == "space":
                y -= row_height(row)
                continue

            if style == "title":
                font = "/F2"
                size = 16
                commands.append("0.08 0.18 0.28 rg")
            elif style == "heading":
                font = "/F2"
                size = 12
                commands.append("0.10 0.24 0.38 rg")
            else:
                font = "/F1"
                size = 10
                commands.append("0.12 0.12 0.12 rg")

            commands.append(f"BT {font} {size} Tf 1 0 0 1 {x} {y} Tm ({_pdf_escape(text)}) Tj ET")
            if style in {"title", "heading"}:
                underline_width = min(len(text) * size * 0.54, page_width - margin - x)
                commands.append("0.10 0.24 0.38 RG")
                commands.append(f"{x} {y - 3} m {x + underline_width:.1f} {y - 3} l S")
            y -= row_height(row)

        commands.extend(
            [
                "0.70 0.78 0.84 RG",
                f"{margin} 56 m {page_width - margin} 56 l S",
                "0.38 0.45 0.52 rg",
                f"BT /F1 8 Tf 1 0 0 1 {margin} 38 Tm (Confidential Executive Report) Tj ET",
                f"BT /F1 8 Tf 1 0 0 1 {page_width - 112} 38 Tm (Page {page_number} of {len(pages)}) Tj ET",
            ]
        )
        stream = "\n".join(commands)
        objects.append(f"<< /Length {len(stream.encode('latin-1', errors='replace'))} >>\nstream\n{stream}\nendstream")

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode())
        pdf.extend(obj.encode("latin-1", errors="replace"))
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode()
    )
    return bytes(pdf)

st.set_page_config(
    page_title="Market Intelligence Platform",
    page_icon="MI",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --mi-ink: #17324d;
            --mi-muted: #5d7087;
            --mi-line: #d8e3ec;
            --mi-surface: #ffffff;
            --mi-soft: #f6fafc;
            --mi-sky: #dff2ff;
            --mi-mint: #dff7ea;
            --mi-coral: #ffded2;
            --mi-gold: #ffe8a3;
            --mi-blue: #1f75cb;
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(223, 242, 255, 0.72), transparent 18rem),
                linear-gradient(135deg, #fbfdff 0%, #f7fbf7 52%, #fffaf2 100%);
            color: var(--mi-ink);
        }

        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer {
            visibility: hidden;
            height: 0;
        }

        .block-container {
            padding-top: 1.2rem;
            max-width: 1180px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #edf7f2 100%);
            border-right: 1px solid var(--mi-line);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--mi-ink);
            letter-spacing: 0;
        }

        h1,
        h2,
        h3 {
            color: var(--mi-ink);
            letter-spacing: 0;
        }

        .block-container h3 {
            font-size: 1.35rem !important;
            line-height: 1.22 !important;
            margin-bottom: 0.45rem !important;
        }

        .block-container p {
            font-size: 0.92rem;
        }

        [data-testid="stSidebar"] .stRadio label,
        .stMarkdown,
        p,
        li,
        label {
            color: var(--mi-muted);
        }

        .mi-hero {
            padding: 0.9rem 1rem !important;
            border: 1px solid var(--mi-line);
            border-radius: 8px;
            background:
                linear-gradient(120deg, rgba(255, 255, 255, 0.96), rgba(246, 250, 252, 0.92)),
                linear-gradient(45deg, rgba(223, 247, 234, 0.45), rgba(223, 242, 255, 0.45));
            box-shadow: 0 8px 20px rgba(23, 50, 77, 0.05);
            margin-bottom: 0.75rem;
        }

        .mi-hero-row {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 1rem;
            align-items: end;
        }

        .mi-kicker {
            color: var(--mi-blue);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.66rem;
            letter-spacing: 0.05rem;
            margin-bottom: 0.35rem;
        }

        .mi-hero .mi-title {
            color: var(--mi-ink);
            font-size: 1.45rem !important;
            line-height: 1.18 !important;
            font-weight: 740 !important;
            letter-spacing: 0 !important;
            max-width: 620px !important;
            margin: 0 0 0.45rem 0 !important;
        }

        .mi-subtitle {
            color: var(--mi-muted);
            max-width: 50rem;
            font-size: 0.86rem;
            line-height: 1.38;
            margin: 0;
        }

        .mi-strip {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.45rem;
            min-width: 18rem;
        }

        .mi-pill {
            border: 1px solid var(--mi-line);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.82);
            padding: 0.38rem 0.62rem;
            color: var(--mi-ink);
            font-size: 0.76rem;
            font-weight: 650;
            min-height: auto;
        }

        div[data-testid="column"] {
            background: rgba(255, 255, 255, 0.68);
            border: 1px solid rgba(216, 227, 236, 0.75);
            border-radius: 8px;
            padding: 0.95rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid var(--mi-line);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 12px 28px rgba(23, 50, 77, 0.06);
        }

        .stButton > button,
        .stDownloadButton > button {
            background: #ffe8a3;
            color: #000000 !important;
            border: 1px solid #e7bd3f;
            border-radius: 8px;
            padding: 0.55rem 1.1rem;
            font-weight: 800 !important;
            box-shadow: 0 10px 22px rgba(231, 189, 63, 0.22);
        }

        .stButton > button p,
        .stDownloadButton > button p {
            color: #000000 !important;
            font-weight: 800 !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: #ffd86a;
            color: #000000 !important;
            border: 1px solid #d3a71f;
        }

        textarea,
        input,
        [data-baseweb="select"] > div,
        [data-testid="stFileUploader"] section {
            border-radius: 8px !important;
            border-color: var(--mi-line) !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid var(--mi-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.82);
        }

        hr {
            border-color: var(--mi-line);
        }

        @media (max-width: 900px) {
            .mi-hero-row {
                grid-template-columns: 1fr;
                align-items: start;
            }

            .mi-strip {
                justify-content: flex-start;
                min-width: 0;
            }
        }

        @media (max-width: 560px) {
            .mi-hero {
                padding: 0.85rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

st.sidebar.title("Market Intelligence")
st.sidebar.markdown("**Agentic research workspace**")

page = st.sidebar.radio(
    "Navigate to",
    ["Home", "Research Dashboard", "Executive Report", "Monitoring Dashboard"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**API Status**")
try:
    health = requests.get(f"{API_BASE}/health", timeout=5).json()
    st.sidebar.success(f"API online - v{health.get('version', '?')}")
except Exception:
    st.sidebar.error("API offline")

# ---------------------------------------------------------------------------
# Page: Home
# ---------------------------------------------------------------------------

if page == "Home":
    st.markdown(
        """
        <section class="mi-hero">
            <div class="mi-hero-row">
                <div>
                    <div class="mi-kicker">Enterprise Business / Market Intelligence</div>
                    <div class="mi-title">Market research agent dashboard</div>
                    <p class="mi-subtitle">
                        Upload documents, run source-backed research, and generate verified executive reports.
                    </p>
                </div>
                <div class="mi-strip">
                    <div class="mi-pill">RAG</div>
                    <div class="mi-pill">Verifier</div>
                    <div class="mi-pill">Summary</div>
                    <div class="mi-pill">Report</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload research documents")
        uploaded_files = st.file_uploader(
            "Upload PDF, DOCX, or TXT files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    resp = requests.post(f"{API_BASE}/upload-document", files=files, timeout=180)
                    if resp.status_code == 200:
                        result = resp.json()
                        st.success(
                            f"Uploaded and indexed: {uploaded_file.name} "
                            f"({result.get('chunks_indexed', 0)} chunks)"
                        )
                    else:
                        st.error(f"Failed to upload {uploaded_file.name}: {resp.text}")
                except Exception as e:
                    st.error(f"Upload error: {e}")

    with col2:
        st.subheader("Quick research query")
        query = st.text_area(
            "Enter your market research question",
            placeholder="e.g. What are the top market trends in Generative AI?",
            height=120,
        )
        if st.button("Run Research", type="primary"):
            if not query.strip():
                st.warning("Please enter a query.")
            else:
                with st.spinner("Running multi-agent research workflow..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/research",
                            json={"query": query, "top_k": 5},
                            timeout=600,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            st.success("Research complete")
                            st.markdown("### Key Insights")
                            st.markdown(data.get("insights", "No insights returned."))
                            st.caption(
                                f"Verified: {'Yes' if data.get('verified') else 'Needs review'} | "
                                f"Latency: {data.get('latency_ms', 0):.0f} ms | "
                                f"Request ID: {data.get('request_id', 'N/A')}"
                            )
                        else:
                            st.error(f"API error {resp.status_code}: {resp.text}")
                    except Exception as e:
                        st.error(f"Request failed: {e}")

# ---------------------------------------------------------------------------
# Page: Research Dashboard
# ---------------------------------------------------------------------------

elif page == "Research Dashboard":
    st.title("Research Dashboard")
    st.markdown("Submit a query to retrieve and verify market insights from your documents.")

    query = st.text_area(
        "Market Research Query",
        placeholder="e.g. Compare Company A and Company B on innovation and market position.",
        height=100,
    )
    top_k = st.slider("Number of source documents to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Run Research Agent", type="primary"):
        if not query.strip():
            st.warning("Please enter a research query.")
        else:
            with st.spinner("Agents working... Research → Verify → Summarize"):
                try:
                    resp = requests.post(
                        f"{API_BASE}/research",
                        json={"query": query, "top_k": top_k},
                        timeout=600,
                    )
                    if resp.status_code == 200:
                        data = resp.json()

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Verified", "Yes" if data.get("verified") else "Needs review")
                        col2.metric("Latency (ms)", f"{data.get('latency_ms', 0):.0f}")
                        col3.metric("Sources Retrieved", len(data.get("sources", [])))

                        st.markdown("---")
                        st.subheader("Key Insights")
                        st.markdown(data.get("insights", "No insights returned."))

                        sources = data.get("sources", [])
                        if sources:
                            st.markdown("---")
                            st.subheader("Retrieved Sources")
                            for i, src in enumerate(sources, 1):
                                with st.expander(f"[{i}] {src.get('source', 'Unknown')} - Page {src.get('page', 'N/A')}"):
                                    st.markdown(src.get("content", ""))
                    else:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# ---------------------------------------------------------------------------
# Page: Executive Report
# ---------------------------------------------------------------------------

elif page == "Executive Report":
    st.title("Executive Report Generator")
    st.markdown(
        "Generate a structured, executive-ready business report with citations "
        "based on your research documents."
    )

    query = st.text_area(
        "Report Topic / Query",
        placeholder="e.g. Generate an executive report on AI adoption in enterprise business.",
        height=100,
    )
    top_k = st.slider("Source documents to use", min_value=1, max_value=10, value=5)

    if st.button("Generate Executive Report", type="primary"):
        if not query.strip():
            st.warning("Please enter a report topic.")
        else:
            with st.spinner("Running full agent pipeline: Research → Verify → Summarize → Report..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/generate-report",
                        json={"query": query, "top_k": top_k},
                        timeout=600,
                    )
                    if resp.status_code == 200:
                        data = resp.json()

                        st.markdown(data.get("report", "No report generated."))

                        citations = data.get("citations", [])
                        if citations:
                            st.markdown("---")
                            st.subheader("Citations")
                            for citation in citations:
                                st.markdown(f"- {citation}")

                        st.caption(
                            f"Latency: {data.get('latency_ms', 0):.0f} ms | "
                            f"Request ID: {data.get('request_id', 'N/A')}"
                        )

                        report_text = data.get("report", "")
                        report_bytes = report_text.encode("utf-8")
                        pdf_bytes = _report_to_pdf(report_text)
                        txt_col, pdf_col = st.columns(2)
                        with txt_col:
                            st.download_button(
                                label="Download Report (TXT)",
                                data=report_bytes,
                                file_name="executive_report.txt",
                                mime="text/plain",
                            )
                        with pdf_col:
                            st.download_button(
                                label="Download Report (PDF)",
                                data=pdf_bytes,
                                file_name="executive_report.pdf",
                                mime="application/pdf",
                            )
                    else:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# ---------------------------------------------------------------------------
# Page: Monitoring Dashboard
# ---------------------------------------------------------------------------

elif page == "Monitoring Dashboard":
    st.title("Monitoring Dashboard")
    st.markdown("Real-time platform usage metrics and application health.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Platform Metrics")
        try:
            metrics = requests.get(f"{API_BASE}/metrics", timeout=10).json()
            st.metric("Total Queries", metrics.get("total_queries", 0))
            st.metric("Total Errors", metrics.get("total_errors", 0))
            st.metric("Avg Latency (ms)", f"{metrics.get('avg_latency_ms', 0):.1f}")
            st.metric("Token Usage (estimate)", metrics.get("token_usage_estimate", 0))
            st.metric("Estimated Cost (USD)", f"${metrics.get('estimated_cost_usd_concept', 0):.6f}")
        except Exception as e:
            st.error(f"Could not load metrics: {e}")

    with col2:
        st.subheader("Simulated Latency Trend")
        import random
        latency_data = [random.uniform(200, 800) for _ in range(20)]
        fig = go.Figure(go.Scatter(y=latency_data, mode="lines+markers", name="Latency (ms)"))
        fig.update_layout(
            xaxis_title="Request #",
            yaxis_title="Latency (ms)",
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Recent Application Logs")
    try:
        logs_resp = requests.get(f"{API_BASE}/logs", timeout=10).json()
        logs = logs_resp.get("logs", [])
        if logs:
            st.code("".join(logs[-20:]), language="text")
        else:
            st.info(logs_resp.get("message", "No logs available."))
    except Exception as e:
        st.error(f"Could not load logs: {e}")
