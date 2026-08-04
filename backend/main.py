"""
FastAPI Backend — Multi-Agent Market Research & Executive Reporting Platform
"""

import ssl_patch  # noqa: F401 — must be first to bypass corporate SSL
from dotenv import load_dotenv
load_dotenv(override=True)

import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

from workflows.langgraph_workflow import run_market_intelligence_workflow
from backend.metrics import metrics_store
from vectorstore.ingest import ingest_file

app = FastAPI(
    title="Market Intelligence API",
    description="Multi-Agent Market Research and Executive Reporting Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ResearchRequest(BaseModel):
    query: str
    top_k: int = 5


class ResearchResponse(BaseModel):
    query: str
    insights: str
    sources: list[dict]
    verified: bool
    request_id: str
    latency_ms: float


class ReportRequest(BaseModel):
    query: str
    top_k: int = 5


class ReportResponse(BaseModel):
    report: str
    citations: list[str]
    request_id: str
    latency_ms: float


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check() -> dict:
    """Returns service health status."""
    return {"status": "healthy", "service": "Market Intelligence API", "version": "1.0.0"}


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest) -> ResearchResponse:
    """
    Accept a user query and return retrieved market insights along with
    verified citations from the document store.
    """
    request_id = str(uuid.uuid4())
    start = time.time()
    logger.info(f"[{request_id}] Research request: {request.query}")

    try:
        result = run_market_intelligence_workflow(
            query=request.query,
            top_k=request.top_k,
            mode="research",
        )
        latency_ms = (time.time() - start) * 1000
        metrics_store.record(latency_ms=latency_ms)

        return ResearchResponse(
            query=request.query,
            insights=result.get("insights", ""),
            sources=result.get("sources", []),
            verified=result.get("verified", False),
            request_id=request_id,
            latency_ms=round(latency_ms, 2),
        )
    except Exception as exc:
        metrics_store.record_error()
        logger.error(f"[{request_id}] Research failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest) -> ReportResponse:
    """
    Generate a full executive-ready report for a given market research query.
    """
    request_id = str(uuid.uuid4())
    start = time.time()
    logger.info(f"[{request_id}] Report generation request: {request.query}")

    try:
        result = run_market_intelligence_workflow(
            query=request.query,
            top_k=request.top_k,
            mode="report",
        )
        latency_ms = (time.time() - start) * 1000
        metrics_store.record(latency_ms=latency_ms)

        return ReportResponse(
            report=result.get("report", ""),
            citations=result.get("citations", []),
            request_id=request_id,
            latency_ms=round(latency_ms, 2),
        )
    except Exception as exc:
        metrics_store.record_error()
        logger.error(f"[{request_id}] Report generation failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)) -> dict:
    """
    Upload and index a research document in the vector store.
    """
    import shutil
    import os

    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }
    file_name = Path(file.filename or "uploaded_document").name
    suffix = Path(file_name).suffix.lower()

    if file.content_type not in allowed_types and suffix not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, or TXT.",
        )

    save_dir = "data/sample_documents"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks_indexed = ingest_file(file_path)
    except Exception as exc:
        logger.error(f"Document uploaded but indexing failed for {file_name}: {exc}")
        raise HTTPException(status_code=500, detail=f"Upload saved, but indexing failed: {exc}") from exc

    logger.info(f"Document uploaded and indexed: {file_name}")
    return {
        "message": f"Document '{file_name}' uploaded and indexed successfully.",
        "path": file_path,
        "chunks_indexed": chunks_indexed,
    }


@app.get("/logs")
def get_logs() -> dict:
    """Return recent application log entries."""
    log_path = "app.log"
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()[-100:]
        return {"logs": lines}
    except FileNotFoundError:
        return {"logs": [], "message": "No log file found yet."}


@app.get("/metrics")
def get_metrics() -> dict:
    """Return platform usage metrics."""
    return metrics_store.summary()
