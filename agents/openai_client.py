"""
Shared OpenAI-compatible client configuration for Azure OpenAI v1 endpoints.
"""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

load_dotenv(override=True)


def _base_url() -> str:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    if endpoint.endswith("/openai/v1"):
        return endpoint
    return f"{endpoint}/openai/v1"


def load_chat_llm() -> ChatOpenAI:
    return ChatOpenAI(
        base_url=_base_url(),
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        temperature=1,
        http_client=httpx.Client(verify=False),
    )


def load_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        base_url=_base_url(),
        model=os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        check_embedding_ctx_length=False,
        http_client=httpx.Client(verify=False),
    )


def embed_texts(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    client = OpenAI(
        base_url=_base_url(),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        http_client=httpx.Client(verify=False),
    )
    model = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small")
    embeddings: list[list[float]] = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        embeddings.extend([item.embedding for item in response.data])

    return embeddings