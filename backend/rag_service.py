import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import chromadb
import httpx
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("rag_service")

class RAGService:
    def __init__(self, persist_dir: str = "./chroma_db", seed_file: str = "../knowledge_base/seed_documents.json"):
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection(
            name="company_kb",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
        self.model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash").strip()

        seed_path = Path(__file__).resolve().parent / seed_file
        if seed_path.exists():
            self.seed_knowledge_base(str(seed_path))

    def seed_knowledge_base(self, seed_file: str):
        with open(seed_file, "r", encoding="utf-8") as f:
            docs = json.load(f)
        for doc in docs:
            self.add_document(doc["id"], doc["title"], doc["content"], doc.get("category", "General"))

    def add_document(self, doc_id: str, title: str, content: str, category: str = "General") -> Dict[str, Any]:
        self.collection.upsert(
            ids=[doc_id],
            documents=[content],
            metadatas=[{"title": title, "category": category}]
        )
        return {"id": doc_id, "title": title, "content": content, "category": category}

    def list_documents(self) -> List[Dict[str, Any]]:
        results = self.collection.get()
        docs = []
        if results and results["ids"]:
            for i in range(len(results["ids"])):
                docs.append({
                    "id": results["ids"][i],
                    "title": results["metadatas"][i].get("title", "Untitled"),
                    "content": results["documents"][i],
                    "category": results["metadatas"][i].get("category", "General")
                })
        return docs

    def delete_document(self, doc_id: str) -> bool:
        existing = self.collection.get(ids=[doc_id])
        if existing and len(existing["ids"]) > 0:
            self.collection.delete(ids=[doc_id])
            return True
        return False

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.collection.count() == 0:
            return []
        
        query_res = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, self.collection.count())
        )
        
        retrieved = []
        if query_res and query_res["documents"] and len(query_res["documents"][0]) > 0:
            for i in range(len(query_res["documents"][0])):
                doc_content = query_res["documents"][0][i]
                metadata = query_res["metadatas"][0][i]
                distance = query_res["distances"][0][i] if "distances" in query_res and query_res["distances"] else 0.0
                
                if distance < 0.90:
                    retrieved.append({
                        "title": metadata.get("title", "Policy Document"),
                        "content": doc_content,
                        "distance": distance
                    })
        return retrieved

    def generate_answer(self, query: str) -> Tuple[str, List[Dict[str, str]]]:
        clean_query = query.strip().lower()
        
        # 1. Polite greeting fallback
        if clean_query in ["hi", "hello", "hey", "good morning", "good afternoon"]:
            return (
                "Hi there! 👋 How can I help you today? Feel free to ask about our remote working policy, VPN setup, password reset, or expense claims.",
                []
            )

        sources = self.retrieve_context(query, top_k=2)

        # 2. Guardrail when no relevant chunks match
        if not sources:
            return (
                "I could not find any policy regarding that in our company knowledge base. "
                "Please consult the HR or IT department directly.",
                []
            )

        context_text = "\n\n".join([f"### Document: {s['title']}\n{s['content']}" for s in sources])

        system_instruction = f"""You are the friendly, helpful, and professional Blacksmith Data AI Knowledge Assistant.

Instructions:
1. Answer the employee's question directly and conversationally using ONLY the provided company knowledge base context.
2. If the context does not contain the answer, explicitly state that the information could not be found in the company knowledge base instead of making up an answer.
3. Keep the tone warm, clear, and complete. Ensure sentences and bullet points are fully finished.

COMPANY KNOWLEDGE BASE CONTEXT:
{context_text}

EMPLOYEE QUESTION:
{query}

ANSWER:"""

        api_key = self.api_key or os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
        if not api_key:
            return (
                "⚠️ API key not found. Please set GEMINI_API_KEY in your backend/.env file.",
                [{"title": s["title"], "content": s["content"]} for s in sources]
            )

        # Candidate models to try in case of temporary 503 high demand spikes
        primary_model = os.getenv("LLM_MODEL", "gemini-2.5-flash").strip()
        candidate_models = [primary_model, "gemini-2.5-flash", "gemini-3.1-flash-lite", "gemini-3.7-flash"]
        # De-duplicate while preserving order
        unique_models = list(dict.fromkeys(candidate_models))

        payload = {
            "contents": [{
                "parts": [{"text": system_instruction}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048  # Increased limit prevents output truncation
            }
        }

        last_error = ""
        with httpx.Client(timeout=20.0) as client:
            for model in unique_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                try:
                    response = client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        answer_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        
                        # Handle cases where the LLM explicitly determines the document does not contain the answer
                        lower_ans = answer_text.lower()
                        fallback_phrases = ["could not be found", "couldn't find", "could not find", "not documented", "no information", "not found"]
                        if any(phrase in lower_ans for phrase in fallback_phrases):
                            return answer_text, []
                            
                        return answer_text, [{"title": s["title"], "content": s["content"]} for s in sources]
                    last_error = response.json().get("error", {}).get("message", response.text)
                    logger.warning(f"Model {model} failed with status {response.status_code}: {last_error}")
                except Exception as e:
                    last_error = str(e)
                    logger.warning(f"Request to {model} failed: {last_error}")

        return f"Gemini API Error: {last_error}", []