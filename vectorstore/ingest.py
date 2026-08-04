"""
Ingest sample documents into the ChromaDB vector store.

Usage:
    python vectorstore/ingest.py

Run this once before starting the application to populate the document store.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ssl_patch  # noqa: F401 — must be first to bypass corporate SSL
import glob
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from loguru import logger
from dotenv import load_dotenv

from agents.openai_client import load_embeddings

load_dotenv(override=True)

DOCUMENTS_DIR = "data/sample_documents"
VECTORSTORE_DIR = "vectorstore"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
SUPPORTED_SUFFIXES = {".pdf", ".docx", ".txt"}


def load_document(file_path: str | Path) -> list:
    path = Path(file_path)
    if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
        return []

    try:
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
        elif path.suffix.lower() == ".docx":
            loader = Docx2txtLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding="utf-8")

        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = path.name
        logger.info(f"Loaded: {path.name} ({len(loaded)} document(s))")
        return loaded
    except Exception as e:
        logger.warning(f"Could not load {path.name}: {e}")
        return []


def load_documents(directory: str) -> list:
    docs = []
    for file_path in glob.glob(f"{directory}/**/*", recursive=True):
        docs.extend(load_document(file_path))
    return docs


def split_documents(raw_docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(raw_docs)


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name="market_intelligence",
        embedding_function=load_embeddings(),
        persist_directory=VECTORSTORE_DIR,
    )


def ingest_file(file_path: str | Path) -> int:
    raw_docs = load_document(file_path)
    if not raw_docs:
        raise ValueError(f"No readable content found in {Path(file_path).name}")

    chunks = split_documents(raw_docs)
    source_name = Path(file_path).name
    vectorstore = get_vectorstore()
    vectorstore._collection.delete(where={"source": source_name})
    vectorstore.add_documents(chunks)
    vectorstore.persist()
    logger.info(f"Indexed uploaded document: {source_name} ({len(chunks)} chunk(s))")
    return len(chunks)


def ingest() -> None:
    logger.info("Starting document ingestion...")

    raw_docs = load_documents(DOCUMENTS_DIR)
    if not raw_docs:
        logger.warning("No documents found. Add files to data/sample_documents/")
        return

    chunks = split_documents(raw_docs)
    logger.info(f"Split into {len(chunks)} chunks.")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=load_embeddings(),
        collection_name="market_intelligence",
        persist_directory=VECTORSTORE_DIR,
    )
    vectorstore.persist()
    logger.info(f"Ingestion complete. {len(chunks)} chunks stored in '{VECTORSTORE_DIR}'.")


if __name__ == "__main__":
    ingest()
