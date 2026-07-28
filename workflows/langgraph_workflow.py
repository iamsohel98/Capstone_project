"""
LangGraph Multi-Agent Workflow — orchestrates Research → Verifier →
Summarizer → Report Generator agents for market intelligence tasks.
"""

from __future__ import annotations

from typing import Any, Literal

from langgraph.graph import StateGraph, END
from loguru import logger

from agents.research_agent import run_research_agent
from agents.verifier_agent import run_verifier_agent
from agents.summarizer_agent import run_summarizer_agent
from agents.report_generator_agent import run_report_generator_agent


# ---------------------------------------------------------------------------
# State type
# ---------------------------------------------------------------------------

WorkflowState = dict[str, Any]


# ---------------------------------------------------------------------------
# Router: decide whether to retry or continue after verification
# ---------------------------------------------------------------------------

def _route_after_verification(state: WorkflowState) -> Literal["summarizer", "research"]:
    """
    If verification fails AND this is the first attempt, retry the research.
    Otherwise proceed to summarization.
    """
    verified: bool = state.get("verified", False)
    retry_count: int = state.get("retry_count", 0)

    if not verified and retry_count < 1:
        logger.info("[Workflow] Verification failed — retrying research (attempt 2).")
        return "research"
    return "summarizer"


def _increment_retry(state: WorkflowState) -> WorkflowState:
    """Increment the retry counter before re-running research."""
    return {**state, "retry_count": state.get("retry_count", 0) + 1}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def _build_research_graph() -> StateGraph:
    """Builds the research-only workflow (Research → Verify → Summarize)."""
    graph = StateGraph(dict)

    graph.add_node("research", run_research_agent)
    graph.add_node("verifier", run_verifier_agent)
    graph.add_node("increment_retry", _increment_retry)
    graph.add_node("summarizer", run_summarizer_agent)

    graph.set_entry_point("research")
    graph.add_edge("research", "verifier")
    graph.add_conditional_edges(
        "verifier",
        _route_after_verification,
        {"research": "increment_retry", "summarizer": "summarizer"},
    )
    graph.add_edge("increment_retry", "research")
    graph.add_edge("summarizer", END)

    return graph


def _build_report_graph() -> StateGraph:
    """Builds the full report workflow (Research → Verify → Summarize → Report)."""
    graph = StateGraph(dict)

    graph.add_node("research", run_research_agent)
    graph.add_node("verifier", run_verifier_agent)
    graph.add_node("increment_retry", _increment_retry)
    graph.add_node("summarizer", run_summarizer_agent)
    graph.add_node("report_generator", run_report_generator_agent)

    graph.set_entry_point("research")
    graph.add_edge("research", "verifier")
    graph.add_conditional_edges(
        "verifier",
        _route_after_verification,
        {"research": "increment_retry", "summarizer": "summarizer"},
    )
    graph.add_edge("increment_retry", "research")
    graph.add_edge("summarizer", "report_generator")
    graph.add_edge("report_generator", END)

    return graph


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_market_intelligence_workflow(
    query: str,
    top_k: int = 5,
    mode: Literal["research", "report"] = "research",
) -> dict[str, Any]:
    """
    Run the multi-agent market intelligence workflow.

    Args:
        query: The user's market research question.
        top_k: Number of document chunks to retrieve.
        mode:  'research' returns summarized insights;
               'report' returns a full executive report.

    Returns:
        Final workflow state dictionary.
    """
    initial_state: WorkflowState = {
        "query": query,
        "top_k": top_k,
        "retry_count": 0,
    }

    if mode == "report":
        graph = _build_report_graph()
    else:
        graph = _build_research_graph()

    app = graph.compile()
    logger.info(f"[Workflow] Starting '{mode}' workflow for query: {query}")

    final_state = app.invoke(initial_state)
    logger.info("[Workflow] Workflow completed.")

    # Normalise output keys for the FastAPI layer
    if mode == "research":
        return {
            "insights": final_state.get("summary", final_state.get("raw_insights", "")),
            "sources": final_state.get("sources", []),
            "verified": final_state.get("verified", False),
        }
    else:
        return {
            "report": final_state.get("report", ""),
            "citations": final_state.get("citations", []),
        }
