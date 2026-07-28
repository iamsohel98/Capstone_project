"""
Research Agent — retrieves and extracts relevant market intelligence
from the vector store using RAG.
"""

from __future__ import annotations

import os
from typing import Any

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from loguru import logger


def _load_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        temperature=0.2,
    )


def _load_vectorstore() -> Chroma:
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    return Chroma(
        collection_name="market_intelligence",
        embedding_function=embeddings,
        persist_directory="vectorstore",
    )


def _build_prompt() -> PromptTemplate:
    template_path = "prompts/research_prompt.txt"
    with open(template_path, "r") as f:
        template = f.read()
    return PromptTemplate(input_variables=["context", "question"], template=template)


def run_research_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Retrieves market intelligence from the document store.

    Args:
        state: LangGraph state containing 'query' and 'top_k'.

    Returns:
        Updated state with 'raw_insights' and 'sources'.
    """
    query: str = state["query"]
    top_k: int = state.get("top_k", 5)

    logger.info(f"[ResearchAgent] Processing query: {query}")

    try:
        llm = _load_llm()
        vectorstore = _load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        prompt = _build_prompt()

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        result = qa_chain.invoke({"query": query})
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])

        sources = [
            {
                "content": doc.page_content[:300],
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "N/A"),
            }
            for doc in source_docs
        ]

        if not answer.strip():
            answer = "The requested information could not be found in the available documents."

        logger.info(f"[ResearchAgent] Retrieved {len(sources)} source(s).")
        return {**state, "raw_insights": answer, "sources": sources}

    except Exception as exc:
        logger.error(f"[ResearchAgent] Error: {exc}")
        return {
            **state,
            "raw_insights": "Research agent encountered an error. Please try again.",
            "sources": [],
            "error": str(exc),
        }
