"""
Tests for the FastAPI backend endpoints.
Run with: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


# ---------------------------------------------------------------------------
# Metrics endpoint
# ---------------------------------------------------------------------------

def test_metrics_returns_expected_keys():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_queries" in data
    assert "total_errors" in data
    assert "avg_latency_ms" in data
    assert "token_usage_estimate" in data
    assert "estimated_cost_usd_concept" in data


# ---------------------------------------------------------------------------
# Logs endpoint
# ---------------------------------------------------------------------------

def test_logs_endpoint():
    response = client.get("/logs")
    assert response.status_code == 200
    data = response.json()
    assert "logs" in data


# ---------------------------------------------------------------------------
# Research endpoint — mocked workflow
# ---------------------------------------------------------------------------

MOCK_RESEARCH_RESULT = {
    "insights": "Generative AI market is growing rapidly at 42% CAGR.",
    "sources": [{"content": "GenAI market...", "source": "genai_trends.txt", "page": "1"}],
    "verified": True,
}


@patch("backend.main.run_market_intelligence_workflow", return_value=MOCK_RESEARCH_RESULT)
def test_research_endpoint_success(mock_workflow):
    response = client.post(
        "/research",
        json={"query": "What are the top GenAI market trends?", "top_k": 3},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What are the top GenAI market trends?"
    assert "insights" in data
    assert "sources" in data
    assert "verified" in data
    assert "request_id" in data
    assert "latency_ms" in data
    mock_workflow.assert_called_once()


@patch(
    "backend.main.run_market_intelligence_workflow",
    side_effect=Exception("LLM unavailable"),
)
def test_research_endpoint_error(mock_workflow):
    response = client.post(
        "/research",
        json={"query": "Test error handling", "top_k": 5},
    )
    assert response.status_code == 500
    assert "detail" in response.json()


def test_research_empty_query():
    """FastAPI Pydantic validation should reject a missing query field."""
    response = client.post("/research", json={"top_k": 5})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Generate report endpoint — mocked workflow
# ---------------------------------------------------------------------------

MOCK_REPORT_RESULT = {
    "report": "# Executive Report\n## Executive Summary\nAI adoption is accelerating...",
    "citations": ["[1] genai_trends.txt — Page 1"],
}


@patch("backend.main.run_market_intelligence_workflow", return_value=MOCK_REPORT_RESULT)
def test_generate_report_endpoint_success(mock_workflow):
    response = client.post(
        "/generate-report",
        json={"query": "AI adoption in enterprise", "top_k": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert "citations" in data
    assert "request_id" in data
    mock_workflow.assert_called_once()


# ---------------------------------------------------------------------------
# Upload endpoint
# ---------------------------------------------------------------------------

def test_upload_document_invalid_type():
    response = client.post(
        "/upload-document",
        files={"file": ("test.exe", b"binary content", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_document_valid_txt(tmp_path):
    content = b"Sample market research content for testing."
    response = client.post(
        "/upload-document",
        files={"file": ("test_doc.txt", content, "text/plain")},
    )
    assert response.status_code == 200
    assert "uploaded successfully" in response.json()["message"]
