"""
Ingest sample documents into the ChromaDB vector store.

Usage:
    python vectorstore/ingest.py

Run this once before starting the application to populate the document store.
"""

import os
import glob
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DOCUMENTS_DIR = "data/sample_documents"
VECTORSTORE_DIR = "vectorstore"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def load_documents(directory: str) -> list:
    docs = []
    for file_path in glob.glob(f"{directory}/**/*", recursive=True):
        path = Path(file_path)
        if not path.is_file():
            continue
        try:
            if path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(path))
            elif path.suffix.lower() == ".docx":
                loader = Docx2txtLoader(str(path))
            elif path.suffix.lower() == ".txt":
                loader = TextLoader(str(path), encoding="utf-8")
            else:
                continue
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = path.name
            docs.extend(loaded)
            logger.info(f"Loaded: {path.name} ({len(loaded)} chunk(s))")
        except Exception as e:
            logger.warning(f"Could not load {path.name}: {e}")
    return docs


def ingest() -> None:
    logger.info("Starting document ingestion...")

    raw_docs = load_documents(DOCUMENTS_DIR)
    if not raw_docs:
        logger.warning("No documents found. Add files to data/sample_documents/")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(raw_docs)
    logger.info(f"Split into {len(chunks)} chunks.")

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="market_intelligence",
        persist_directory=VECTORSTORE_DIR,
    )
    vectorstore.persist()
    logger.info(f"Ingestion complete. {len(chunks)} chunks stored in '{VECTORSTORE_DIR}'.")


if __name__ == "__main__":
    ingest()
