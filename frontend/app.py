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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

st.sidebar.title("📊 Market Intelligence")
st.sidebar.markdown("**Multi-Agent AI Platform**")

page = st.sidebar.radio(
    "Navigate to",
    ["🏠 Home", "🔍 Research Dashboard", "📋 Executive Report", "📈 Monitoring Dashboard"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**API Status**")
try:
    health = requests.get(f"{API_BASE}/health", timeout=5).json()
    st.sidebar.success(f"✅ API Online — v{health.get('version', '?')}")
except Exception:
    st.sidebar.error("❌ API Offline")

# ---------------------------------------------------------------------------
# Page: Home
# ---------------------------------------------------------------------------

if page == "🏠 Home":
    st.title("📊 Enterprise Business / Market Intelligence")
    st.subheader("Multi-Agent Market Research and Executive Reporting Platform")
    st.markdown(
        """
        This platform uses a **multi-agent AI workflow** to help business teams:
        - 🔍 Retrieve insights from research documents
        - ✅ Verify facts against source material
        - 📝 Summarise industry trends and competitor insights
        - 📋 Generate executive-ready business reports with citations
        """
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📂 Upload Research Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF, DOCX, or TXT files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    resp = requests.post(f"{API_BASE}/upload-document", files=files, timeout=30)
                    if resp.status_code == 200:
                        st.success(f"✅ Uploaded: {uploaded_file.name}")
                    else:
                        st.error(f"❌ Failed to upload {uploaded_file.name}: {resp.text}")
                except Exception as e:
                    st.error(f"❌ Upload error: {e}")

    with col2:
        st.subheader("🔍 Quick Research Query")
        query = st.text_area(
            "Enter your market research question",
            placeholder="e.g. What are the top market trends in Generative AI?",
            height=120,
        )
        if st.button("🚀 Run Research", type="primary"):
            if not query.strip():
                st.warning("Please enter a query.")
            else:
                with st.spinner("Running multi-agent research workflow..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/research",
                            json={"query": query, "top_k": 5},
                            timeout=120,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            st.success("✅ Research complete!")
                            st.markdown("### Key Insights")
                            st.markdown(data.get("insights", "No insights returned."))
                            st.caption(
                                f"Verified: {'✅' if data.get('verified') else '⚠️ Unverified'} | "
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

elif page == "🔍 Research Dashboard":
    st.title("🔍 Research Dashboard")
    st.markdown("Submit a query to retrieve and verify market insights from your documents.")

    query = st.text_area(
        "Market Research Query",
        placeholder="e.g. Compare Company A and Company B on innovation and market position.",
        height=100,
    )
    top_k = st.slider("Number of source documents to retrieve", min_value=1, max_value=10, value=5)

    if st.button("🔍 Run Research Agent", type="primary"):
        if not query.strip():
            st.warning("Please enter a research query.")
        else:
            with st.spinner("Agents working... Research → Verify → Summarize"):
                try:
                    resp = requests.post(
                        f"{API_BASE}/research",
                        json={"query": query, "top_k": top_k},
                        timeout=180,
                    )
                    if resp.status_code == 200:
                        data = resp.json()

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Verified", "✅ Yes" if data.get("verified") else "⚠️ No")
                        col2.metric("Latency (ms)", f"{data.get('latency_ms', 0):.0f}")
                        col3.metric("Sources Retrieved", len(data.get("sources", [])))

                        st.markdown("---")
                        st.subheader("📝 Key Insights")
                        st.markdown(data.get("insights", "No insights returned."))

                        sources = data.get("sources", [])
                        if sources:
                            st.markdown("---")
                            st.subheader("📚 Retrieved Sources")
                            for i, src in enumerate(sources, 1):
                                with st.expander(f"[{i}] {src.get('source', 'Unknown')} — Page {src.get('page', 'N/A')}"):
                                    st.markdown(src.get("content", ""))
                    else:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# ---------------------------------------------------------------------------
# Page: Executive Report
# ---------------------------------------------------------------------------

elif page == "📋 Executive Report":
    st.title("📋 Executive Report Generator")
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

    if st.button("📋 Generate Executive Report", type="primary"):
        if not query.strip():
            st.warning("Please enter a report topic.")
        else:
            with st.spinner("Running full agent pipeline: Research → Verify → Summarize → Report..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/generate-report",
                        json={"query": query, "top_k": top_k},
                        timeout=300,
                    )
                    if resp.status_code == 200:
                        data = resp.json()

                        st.markdown(data.get("report", "No report generated."))

                        citations = data.get("citations", [])
                        if citations:
                            st.markdown("---")
                            st.subheader("📖 Citations")
                            for citation in citations:
                                st.markdown(f"- {citation}")

                        st.caption(
                            f"Latency: {data.get('latency_ms', 0):.0f} ms | "
                            f"Request ID: {data.get('request_id', 'N/A')}"
                        )

                        report_bytes = data.get("report", "").encode("utf-8")
                        st.download_button(
                            label="⬇️ Download Report (TXT)",
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

elif page == "📈 Monitoring Dashboard":
    st.title("📈 Monitoring Dashboard")
    st.markdown("Real-time platform usage metrics and application health.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Platform Metrics")
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
        st.subheader("📉 Simulated Latency Trend")
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
    st.subheader("📋 Recent Application Logs")
    try:
        logs_resp = requests.get(f"{API_BASE}/logs", timeout=10).json()
        logs = logs_resp.get("logs", [])
        if logs:
            st.code("".join(logs[-20:]), language="text")
        else:
            st.info(logs_resp.get("message", "No logs available."))
    except Exception as e:
        st.error(f"Could not load logs: {e}")
