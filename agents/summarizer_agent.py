"""
Summarizer Agent — converts raw research insights into concise,
business-friendly summaries covering trends, risks, and opportunities.
"""
from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from agents.openai_client import load_chat_llm


_SUMMARIZER_SYSTEM = """You are an expert business analyst. 
Your task is to convert raw market research insights into a clear, concise business summary.

Structure your response with these sections (use only those relevant to the content):
- **Key Findings**: 3-5 bullet points of the most important insights.
- **Industry Trends**: Notable patterns or directions in the market.
- **Competitive Landscape**: Brief notes on competitor positioning if mentioned.
- **Opportunities**: Areas where the business can grow or differentiate.
- **Risks**: Potential threats or challenges identified.

Keep the language professional and executive-friendly. Be concise."""

_SUMMARIZER_HUMAN = """Raw Research Insights:
{raw_insights}

Query: {query}

Please summarize the above insights into a structured business summary."""


def run_summarizer_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Summarizes raw insights into structured business content.

    Args:
        state: LangGraph state containing 'raw_insights' and 'query'.

    Returns:
        Updated state with 'summary'.
    """
    raw_insights: str = state.get("raw_insights", "")
    query: str = state.get("query", "")

    logger.info("[SummarizerAgent] Generating business summary.")

    if state.get("error"):
        return {
            **state,
            "summary": (
                "Research could not be completed because the document retrieval step failed. "
                f"Error: {state.get('error')}"
            ),
        }

    if (
        not raw_insights.strip()
        or "could not be found" in raw_insights.lower()
        or "research agent encountered an error" in raw_insights.lower()
    ):
        return {
            **state,
            "summary": "Insufficient information found in documents to generate a meaningful summary.",
        }

    try:
        llm = load_chat_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", _SUMMARIZER_SYSTEM),
            ("human", _SUMMARIZER_HUMAN),
        ])
        chain = prompt | llm

        response = chain.invoke({"raw_insights": raw_insights, "query": query})
        summary = response.content.strip()

        logger.info("[SummarizerAgent] Summary generated successfully.")
        return {**state, "summary": summary}

    except Exception as exc:
        logger.error(f"[SummarizerAgent] Error: {exc}")
        return {
            **state,
            "summary": f"Summary generation failed: {exc}",
        }
