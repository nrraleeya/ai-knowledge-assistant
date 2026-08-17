import pytest
from fastapi.testclient import TestClient
from main import app
from rag_service import RAGService

client = TestClient(app)

# ---------------------------------------------------------------------------
# 1. Document Retrieval & Vector Store Tests
# ---------------------------------------------------------------------------

def test_document_retrieval_semantic_match():
    """Verify that vector retrieval returns the correct policy chunk for a query."""
    rag = RAGService(persist_dir="./chroma_db")
    
    # Query semantic match for remote work
    results = rag.retrieve_context("work from home rules for interns", top_k=2)
    
    assert len(results) > 0
    assert any("Flexible & Remote Working Policy" in doc["title"] for doc in results)
    assert any("interns" in doc["content"].lower() for doc in results)

def test_document_retrieval_it_support():
    """Verify retrieval for IT support queries like password reset."""
    rag = RAGService(persist_dir="./chroma_db")
    
    results = rag.retrieve_context("how do I reset my password?", top_k=2)
    
    assert len(results) > 0
    assert any("Password Reset" in doc["title"] for doc in results)

# ---------------------------------------------------------------------------
# 2. Document Management API Endpoints
# ---------------------------------------------------------------------------

def test_get_all_documents_api():
    """Verify GET /api/documents returns the seeded knowledge base."""
    response = client.get("/api/documents")
    assert response.status_code == 200
    docs = response.json()
    assert isinstance(docs, list)
    assert len(docs) >= 1

def test_add_and_delete_document_lifecycle():
    """Verify adding a new policy and deleting it via the API."""
    new_doc = {
        "id": "doc-test-99",
        "title": "Gym Membership Subsidy",
        "content": "Employees are eligible for a $40 monthly gym reimbursement.",
        "category": "Benefits"
    }
    
    # 1. Create document
    create_res = client.post("/api/documents", json=new_doc)
    assert create_res.status_code == 201
    assert create_res.json()["id"] == "doc-test-99"

    # 2. Delete document
    delete_res = client.delete("/api/documents/doc-test-99")
    assert delete_res.status_code == 200
    assert "successfully deleted" in delete_res.json()["message"]

# ---------------------------------------------------------------------------
# 3. End-to-End RAG Scenarios
# ---------------------------------------------------------------------------

def test_rag_in_scope_wfh_query():
    """RAG Scenario 1: In-scope query must retrieve sources and generate grounded answer."""
    response = client.post("/api/chat", json={
        "message": "What is the core working hours for Blacksmith Data?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert answer contains verified policy facts
    assert "10:00" in data["answer"] or "4:00" in data["answer"]
    
    # Assert source citations are attached
    assert len(data["sources"]) > 0
    assert "Flexible & Remote Working Policy" in data["sources"][0]["title"]

def test_rag_out_of_scope_guardrail():
    """RAG Scenario 2: Out-of-scope query must trigger fallback without hallucinating."""
    response = client.post("/api/chat", json={
        "message": "What is the company stock option and equity vesting schedule?"
    })
    
    assert response.status_code == 200
    data = response.json()
    answer = data["answer"].lower()
    
    # Assert graceful fallback message is returned
    fallback_keywords = ["couldn't find", "could not find", "not documented", "no information", "not found", "don't have"]
    assert any(keyword in answer for keyword in fallback_keywords), f"Unexpected response: {data['answer']}"
    
    # Guardrail ensures no misleading sources are cited
    assert len(data["sources"]) == 0