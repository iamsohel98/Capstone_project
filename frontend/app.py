"""
Streamlit Frontend — Multi-Agent Market Research & Executive Reporting Platform
"""

import io
import os

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")

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
            background: var(--mi-blue);
            color: #ffffff;
            border: 0;
            border-radius: 8px;
            padding: 0.55rem 1.1rem;
            font-weight: 700;
            box-shadow: 0 10px 22px rgba(31, 117, 203, 0.22);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: #185fa6;
            color: #ffffff;
            border: 0;
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

                        report_bytes = data.get("report", "").encode("utf-8")
                        st.download_button(
                            label="Download Report (TXT)",
                            data=report_bytes,
                            file_name="executive_report.txt",
                            mime="text/plain",
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
