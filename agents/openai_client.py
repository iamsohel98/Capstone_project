"""
Shared OpenAI-compatible client configuration for Azure OpenAI v1 endpoints.
"""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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
        http_client=httpx.Client(verify=False),
    )


def load_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        base_url=_base_url(),
        model=os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        http_client=httpx.Client(verify=False),
    )