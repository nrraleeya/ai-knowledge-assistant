import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from rag_service import RAGService

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ai_assistant")

app = FastAPI(
    title="AI Knowledge Assistant API",
    description="RAG-powered Knowledge Base API with Document Management and Hallucination Guardrails",
    version="1.0.0"
)

# Enable CORS for Frontend SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_service = RAGService()

# Pydantic Schemas
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Employee question")

class SourceCitation(BaseModel):
    title: str
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]

class DocumentCreateRequest(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=5)
    category: Optional[str] = "General"

class DocumentItem(BaseModel):
    id: str
    title: str
    content: str
    category: str

# API Endpoints
@app.post("/api/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Incoming chat query: {request.message}")
    try:
        answer, sources = rag_service.generate_answer(request.message)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate answer from knowledge base."
        )

@app.get("/api/documents", response_model=List[DocumentItem], status_code=status.HTTP_200_OK)
async def get_documents():
    return rag_service.list_documents()

@app.post("/api/documents", response_model=DocumentItem, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreateRequest):
    logger.info(f"Adding/Updating document ID: {doc.id}")
    created = rag_service.add_document(doc.id, doc.title, doc.content, doc.category or "General")
    return DocumentItem(**created)

@app.delete("/api/documents/{doc_id}", status_code=status.HTTP_200_OK)
async def delete_document(doc_id: str):
    logger.info(f"Deleting document ID: {doc_id}")
    success = rag_service.delete_document(doc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{doc_id}' not found."
        )
    return {"message": f"Document '{doc_id}' successfully deleted."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)