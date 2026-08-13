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
import uuid
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from loguru import logger
from dotenv import load_dotenv

from agents.openai_client import embed_texts, load_embeddings

load_dotenv(override=True)

DOCUMENTS_DIR = "data/sample_documents"
VECTORSTORE_DIR = "vectorstore"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
SUPPORTED_SUFFIXES = {".pdf", ".docx", ".txt"}


def load_document(file_path: str | Path) -> list:
    # Pick the right LangChain loader based on file extension (PDF/DOCX/TXT)
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
        # Tag each doc with its filename so retrieved chunks can be traced back to a source
        for doc in loaded:
            doc.metadata["source"] = path.name
        logger.info(f"Loaded: {path.name} ({len(loaded)} document(s))")
        return loaded
    except Exception as e:
        logger.warning(f"Could not load {path.name}: {e}")
        return []


def load_documents(directory: str) -> list:
    # Recursively load every supported file under the sample documents directory
    docs = []
    for file_path in glob.glob(f"{directory}/**/*", recursive=True):
        docs.extend(load_document(file_path))
    return docs


def split_documents(raw_docs: list) -> list:
    # Break documents into overlapping chunks so retrieval returns focused, relevant context
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(raw_docs)


def get_vectorstore() -> Chroma:
    # Connect to the persisted Chroma collection used for RAG retrieval
    return Chroma(
        collection_name="market_intelligence",
        embedding_function=load_embeddings(),
        persist_directory=VECTORSTORE_DIR,
    )


def _clean_metadata(metadata: dict) -> dict:
    return {
        str(key): "" if value is None else str(value)
        for key, value in metadata.items()
    }


def ingest_file(file_path: str | Path) -> int:
    # Incrementally index a single uploaded file into the RAG vector store
    raw_docs = load_document(file_path)
    if not raw_docs:
        raise ValueError(f"No readable content found in {Path(file_path).name}")

    chunks = split_documents(raw_docs)
    source_name = Path(file_path).name
    vectorstore = get_vectorstore()
    # Remove any stale chunks from a previous version of this same file before re-adding
    vectorstore._collection.delete(where={"source": source_name})

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [_clean_metadata(chunk.metadata) for chunk in chunks]
    ids = [f"{source_name}-{uuid.uuid4()}" for _ in chunks]
    embeddings = embed_texts(texts)

    vectorstore._collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    vectorstore.persist()
    logger.info(f"Indexed uploaded document: {source_name} ({len(chunks)} chunk(s))")
    return len(chunks)


def ingest() -> None:
    # Bulk (re)build of the vector store from all sample documents on disk
    logger.info("Starting document ingestion...")

    raw_docs = load_documents(DOCUMENTS_DIR)
    if not raw_docs:
        logger.warning("No documents found. Add files to data/sample_documents/")
        return

    chunks = split_documents(raw_docs)
    logger.info(f"Split into {len(chunks)} chunks.")

    vectorstore = get_vectorstore()
    # Wipe the existing collection so re-running ingestion doesn't duplicate chunks
    vectorstore._collection.delete()

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [_clean_metadata(chunk.metadata) for chunk in chunks]
    ids = [f"bulk-{uuid.uuid4()}" for _ in chunks]
    embeddings = embed_texts(texts)

    vectorstore._collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    vectorstore.persist()
    logger.info(f"Ingestion complete. {len(chunks)} chunks stored in '{VECTORSTORE_DIR}'.")


if __name__ == "__main__":
    ingest()
