"""
Report Generator Agent — produces a structured, executive-ready business
report with citations from the summarized insights and verified sources.
"""

from __future__ import annotations

import os
from typing import Any

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger


_REPORT_SYSTEM = """You are a senior management consultant writing an executive business report.

Your report must follow this structure:

---
# Executive Report: {title}

## Executive Summary
A concise 2-3 sentence overview of the key findings.

## Industry Overview
Background on the market and industry context.

## Competitor Analysis
Analysis of key competitors and their positioning (if information is available).

## Market Opportunities
Specific opportunities identified from the research.

## Risks and Challenges
Potential risks, threats, or challenges.

## Strategic Recommendations
3-5 clear, actionable recommendations for leadership.

## Citations and References
List all referenced sources using the format [n] Source: <filename>, Page: <page>.
---

Rules:
- Every factual claim must be supported by the provided sources.
- Use professional, executive-level language.
- If information is not available in the sources, state "Information not available in current documents."
- Do not fabricate data or statistics.
- Always include citations."""

_REPORT_HUMAN = """Query / Topic: {query}

Summarized Insights:
{summary}

Verified Sources:
{sources}

Please generate a complete executive report following the structure above."""


def _load_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        temperature=0.3,
    )


def _format_sources(sources: list[dict]) -> str:
    if not sources:
        return "No verified sources available."
    return "\n".join(
        f"[{i+1}] Source: {s.get('source', 'unknown')}, Page: {s.get('page', 'N/A')}\n"
        f"    Excerpt: {s.get('content', '')[:200]}..."
        for i, s in enumerate(sources)
    )


def _extract_citations(sources: list[dict]) -> list[str]:
    return [
        f"[{i+1}] {s.get('source', 'unknown')} — Page {s.get('page', 'N/A')}"
        for i, s in enumerate(sources)
    ]


def run_report_generator_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Generates an executive-ready business report.

    Args:
        state: LangGraph state containing 'summary', 'sources', and 'query'.

    Returns:
        Updated state with 'report' and 'citations'.
    """
    summary: str = state.get("summary", "")
    sources: list[dict] = state.get("sources", [])
    query: str = state.get("query", "Market Intelligence Report")

    logger.info("[ReportGeneratorAgent] Generating executive report.")

    if not summary.strip():
        return {
            **state,
            "report": "Unable to generate report: no summarized insights available.",
            "citations": [],
        }

    try:
        llm = _load_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", _REPORT_SYSTEM),
            ("human", _REPORT_HUMAN),
        ])
        chain = prompt | llm

        response = chain.invoke({
            "title": query,
            "query": query,
            "summary": summary,
            "sources": _format_sources(sources),
        })

        report = response.content.strip()
        citations = _extract_citations(sources)

        logger.info("[ReportGeneratorAgent] Executive report generated successfully.")
        return {**state, "report": report, "citations": citations}

    except Exception as exc:
        logger.error(f"[ReportGeneratorAgent] Error: {exc}")
        return {
            **state,
            "report": f"Report generation failed: {exc}",
            "citations": [],
        }
