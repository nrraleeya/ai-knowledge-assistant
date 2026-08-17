# Blacksmith Data - AI Knowledge Assistant

An enterprise RAG-powered Knowledge Assistant designed to answer internal employee questions accurately with strict document source citations and hallucination guardrails.

## 1. Project Overview
The AI Knowledge Assistant allows employees to search internal company policies (WFH rules, IT troubleshooting, expense claims, onboarding) using natural language. The backend retrieves the most relevant policy documents from a vector store and synthesizes grounded answers using an LLM.

## 2. Architecture
The system employs a 3-tier architecture with clean separation:
- **Presentation Layer**: React (Vite + Tailwind CSS) providing responsive chat, loading indicators, and source citations.
- **Application Layer**: FastAPI backend with Pydantic request validation and error handling.
- **Data & AI Layer**: ChromaDB vector store paired with Sentence-Transformers for semantic embeddings and Google Gemini for grounded generation.

## 3. Technology Choices
- **FastAPI (Python)**: High-performance asynchronous REST API with native Pydantic validation.
- **React + Tailwind CSS**: Clean, fast, and responsive user experience for multi-turn conversations.
- **ChromaDB**: In-process, zero-configuration vector store ensuring reproducible local evaluation.
- **all-MiniLM-L6-v2**: High-speed, local CPU-based embedding model eliminating embedding API costs.
- **Google Gemini 1.5 Flash**: Low-latency, generous free-tier LLM for grounded context reasoning.

## 4. Setup Instructions
### Prerequisites
- Python 3.10+
- Node.js 18+

### Clone & Install Backend
```bash
git clone <your-repo-link>
cd project/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt