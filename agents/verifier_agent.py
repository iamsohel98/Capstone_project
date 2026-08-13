"""
Verifier Agent — validates that generated insights are grounded in
the retrieved source documents and flags unsupported claims
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from agents.openai_client import load_chat_llm


_VERIFIER_SYSTEM = """You are a strict fact-checking assistant.
Your task is to verify whether the provided ANSWER is fully supported by the SOURCE EXCERPTS.

Rules:
- If every key claim in the ANSWER can be traced back to the SOURCE EXCERPTS, respond with VERIFIED.
- If any claim is not supported, respond with UNVERIFIED and list the unsupported claims.
- Never add information that is not in the sources.
- Always be concise and precise.
"""

_VERIFIER_HUMAN = """SOURCE EXCERPTS:
{sources}

ANSWER:
{answer}

Is the answer fully supported by the sources? Respond with VERIFIED or UNVERIFIED followed by a brief explanation."""


def run_verifier_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Checks whether the raw_insights are grounded in the retrieved sources.

    Args:
        state: LangGraph state containing 'raw_insights' and 'sources'.

    Returns:
        Updated state with 'verified' (bool) and 'verification_note' (str).
    """
    raw_insights: str = state.get("raw_insights", "")
    sources: list[dict] = state.get("sources", [])

    logger.info("[VerifierAgent] Starting fact verification.")

    if not raw_insights.strip():
        return {**state, "verified": False, "verification_note": "No insights to verify."}

    if not sources:
        return {
            **state,
            "verified": False,
            "verification_note": "No source documents available for verification.",
        }

    source_text = "\n\n".join(
        f"[{i+1}] ({s.get('source', 'unknown')}) {s.get('content', '')}"
        for i, s in enumerate(sources)
    )

    try:
        llm = load_chat_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", _VERIFIER_SYSTEM),
            ("human", _VERIFIER_HUMAN),
        ])
        chain = prompt | llm

        response = chain.invoke({"sources": source_text, "answer": raw_insights})
        verdict_text: str = response.content.strip()

        verified = verdict_text.upper().startswith("VERIFIED")
        logger.info(f"[VerifierAgent] Verdict: {'VERIFIED' if verified else 'UNVERIFIED'}")

        return {**state, "verified": verified, "verification_note": verdict_text}

    except Exception as exc:
        logger.error(f"[VerifierAgent] Error: {exc}")
        return {
            **state,
            "verified": False,
            "verification_note": f"Verification failed due to an error: {exc}",
        }
