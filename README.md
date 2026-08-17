# Blacksmith Data · AI Knowledge Assistant

An end-to-end Retrieval-Augmented Generation (RAG) assistant designed for internal employees to query company policies, IT workflows, and onboarding guidelines with verifiable citations and strict hallucination guardrails.

---

## 🌐 Live Interactive Demo

Reviewers and team members can test the application live on mobile or desktop without local setup:

* **🚀 Live Web App (Frontend):** https://ai-knowledge-assistant-silk.vercel.app
* **📚 Interactive Swagger API Docs (Backend):** https://ai-knowledge-assistant-backend-6dtu.onrender.com/docs

> **Note on Free-Tier Hosting:** The backend is deployed on Render's free tier. If idle for 15 minutes, the instance spins down. The first query after spin-down may take ~30–45 seconds to wake the service; subsequent requests respond instantly.

---

## 1. Project Overview

The **Blacksmith Data AI Knowledge Assistant** provides employees with real-time, accurate answers to organizational questions (such as remote work rules, VPN setups, expense claims, and onboarding schedules)[cite: 1, 2].

### Key Highlights
* **Grounded Synthesis:** Formulates answers strictly using retrieved company policy documents[cite: 1, 2].
* **Verifiable Source Attribution:** Displays collapsible citation badges with exact document titles and source excerpts[cite: 1, 2].
* **Anti-Hallucination Guardrails:** Distinguishes between in-scope queries and undocumented questions, falling back safely without inventing policies[cite: 1, 2].
* **Live Knowledge Base Management:** REST endpoints to dynamically query, index, and purge policy documents at runtime[cite: 1, 2].

---

## 2. Architecture

The system enforces modular separation between the presentation tier, backend API routing, vector database persistence, and external LLM reasoning[cite: 1, 2].

### Architecture Concept Map

```mermaid
graph TD
    subgraph Presentation_Tier [Presentation Tier - Vercel]
        UI[React 18 + Vite Web App]
        Chat[Responsive Chat Interface]
        Sources[Collapsible Source Accordion]
        UI --> Chat
        UI --> Sources
    end

    subgraph Backend_Tier [Backend API - Render]
        API[FastAPI Application]
        Validation[Pydantic v2 Schema Validation]
        Endpoints[REST Endpoints: /api/chat, /api/documents]
        API --> Validation
        API --> Endpoints
    end

    subgraph Data_Tier [Data Tier]
        Chroma[(ChromaDB Persistent Store)]
        SeedData[Seed Policies: HR, IT, Ops, Finance]
        Chroma --- SeedData
    end

    subgraph AI_Tier [AI Reasoning Tier]
        Gemini[Google Gemini API]
        Model[gemini-2.5-flash Engine]
        Gemini --- Model
    end

    UI <-->|HTTPS JSON Requests| API
    Endpoints <-->|Cosine Distance Retrieval| Chroma
    Endpoints <-->|Bounded Grounding Prompt & Synthesis| Gemini
```

### Visual Component Flow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION TIER                              │
│   React 18 + Vite Web App (Deployed on Vercel)                              │
│   ├── Responsive Chat Interface (Dark Theme with Rose Accents)              │
│   ├── Collapsible Source Citation Cards                                     │
│   └── Real-time Loading Animations & Connection Error Alerts                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS (JSON API)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 BACKEND API                                 │
│   FastAPI Application (Deployed on Render)                                  │
│   ├── REST Endpoints (/api/chat, /api/documents)                            │
│   ├── Pydantic Request/Response Validation                                  │
│   ├── CORS Middleware & Error Handlers                                      │
│   └── Structured Logging & Telemetry                                        │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│              DATA TIER               │ │              AI TIER               │
│   ChromaDB Persistent Store          │ │   Google Gemini API                │
│   ├── HNSW Cosine Distance Index     │ │   ├── gemini-2.5-flash             │
│   └── Seed Policies (HR, IT, Ops)    │ │   └── Strict Grounding Prompts     │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

---

## 3. Technology Choices

| Layer | Technology | Selection Rationale |
| :--- | :--- | :--- |
| **Frontend** | **React 18 + Vite**[cite: 1, 2] | Rapid build times, fast Hot Module Replacement (HMR), minimal bundle footprint, and efficient component-driven state management[cite: 1, 2]. |
| **Styling** | **Tailwind CSS** | Clean responsive UI layout, dark-mode styling, and mobile-friendly utility classes. |
| **Backend** | **FastAPI (Python)**[cite: 1, 2] | High asynchronous performance, native Pydantic schema validation, and automatic Swagger UI docs generation[cite: 1, 2]. |
| **Database / Vector Store** | **ChromaDB**[cite: 1, 2] | Native Python integration, zero external operational overhead, disk persistence, and built-in HNSW cosine similarity search[cite: 1, 2]. |
| **LLM Provider** | **Google Gemini (2.5 Flash)**[cite: 1, 2] | Fast generation speed, strict context adherence, generous rate limits, and free-tier access[cite: 1, 2]. |
| **HTTP Client** | **HTTPX** | Asynchronous HTTP client with connection pooling, timeout controls, and multi-model fallback resiliency. |
| **Testing** | **Pytest + TestClient**[cite: 1, 2] | Fast, deterministic automated testing and assertions for API endpoints and RAG flows[cite: 1, 2]. |

---

## 4. Setup Instructions

### Prerequisites
* **Python 3.10+** (`python --version`)
* **Node.js 18+** & **npm** (`node -v` && `npm -v`)
* **Git** installed on your system
* A free **Google AI Studio API Key**[cite: 1, 2]

### Clone Repository
```bash
git clone [https://github.com/nrraleeya/ai-knowledge-assistant.git](https://github.com/nrraleeya/ai-knowledge-assistant.git)
cd ai-knowledge-assistant
```

---

## 5. Environment Variables

Create a `.env` file inside the `backend/` directory using the provided `.env.example`[cite: 1, 2]:

```bash
cd backend
cp .env.example .env
```

Set the required environment variables inside `backend/.env`[cite: 1, 2]:
```env
# Required: Google Gemini API Key from Google AI Studio
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Preferred model name (default: gemini-2.5-flash)
LLM_MODEL=gemini-2.5-flash
```

---

## 6. How to Run the Frontend

Open a terminal window and run[cite: 1, 2]:

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

* **Frontend Local URL:** `http://localhost:5173`

---

## 7. How to Run the Backend

Open a separate terminal window and run[cite: 1, 2]:

```bash
# 1. Navigate to backend directory
cd backend

# 2. (Recommended) Activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

* **Backend Local API:** `http://localhost:8000`[cite: 1, 2]
* **Swagger UI Documentation:** `http://localhost:8000/docs`
* **ReDoc Documentation:** `http://localhost:8000/redoc`

---

## 8. How to Run Tests

The automated test suite verifies API request schemas, document CRUD lifecycles, semantic vector retrieval, grounded answering, and unknown question guardrails[cite: 1, 2].

Run pytest inside the `backend/` directory[cite: 1, 2]:
```bash
cd backend
pytest -v
```

Expected test output[cite: 1, 2]:
```text
test_app.py::test_document_retrieval_semantic_match PASSED        [ 16%]
test_app.py::test_document_retrieval_it_support PASSED            [ 33%]
test_app.py::test_get_all_documents_api PASSED                    [ 50%]
test_app.py::test_add_and_delete_document_lifecycle PASSED        [ 66%]
test_app.py::test_rag_in_scope_wfh_query PASSED                   [ 83%]
test_app.py::test_rag_out_of_scope_guardrail PASSED               [100%]

============================== 6 passed in 8.12s ==============================
```

---

## 9. API Documentation

### 1. Submit Chat Message
* **Endpoint:** `POST /api/chat`[cite: 1, 2]
* **Request Body:**[cite: 1, 2]
  ```json
  {
    "message": "What is the core working hours policy?"
  }
  ```
* **Success Response (`200 OK`):**[cite: 1, 2]
  ```json
  {
    "answer": "Core collaboration hours are 10:00 AM to 4:00 PM local time. Employees are expected to be available for team communications and scheduled meetings during this window.",
    "sources": [
      {
        "title": "Flexible & Remote Working Policy",
        "content": "Core collaboration hours are 10:00 AM to 4:00 PM local time..."
      }
    ]
  }
  ```

### 2. List All Indexed Documents
* **Endpoint:** `GET /api/documents`[cite: 1, 2]
* **Response (`200 OK`):**[cite: 1, 2]
  ```json
  [
    {
      "id": "doc-wfh-01",
      "title": "Flexible & Remote Working Policy",
      "category": "Human Resources",
      "content": "Employees may work remotely up to 3 days per week..."
    }
  ]
  ```

### 3. Add / Index a New Document
* **Endpoint:** `POST /api/documents`[cite: 1, 2]
* **Request Body:**[cite: 1, 2]
  ```json
  {
    "id": "doc-parking-01",
    "title": "Office Parking Policy",
    "category": "Facilities",
    "content": "Employee parking passes are available for Basement Level 2."
  }
  ```
* **Response (`201 Created`):**[cite: 1, 2]
  ```json
  {
    "id": "doc-parking-01",
    "title": "Office Parking Policy",
    "category": "Facilities",
    "content": "Employee parking passes are available for Basement Level 2."
  }
  ```

### 4. Delete a Document
* **Endpoint:** `DELETE /api/documents/{doc_id}`[cite: 1, 2]
* **Response (`200 OK`):**[cite: 1, 2]
  ```json
  {
    "message": "Document doc-parking-01 successfully deleted."
  }
  ```

---

## 10. RAG Implementation

### RAG Pipeline & Guardrail Sequence Diagram

```mermaid
sequenceDiagram
    participant U as Employee (Client UI)
    participant API as FastAPI Backend
    participant VDB as ChromaDB
    participant LLM as Gemini API

    U->>API: POST /api/chat {"message": "..."}
    API->>VDB: Embed query & Search HNSW Index
    VDB-->>API: Return Top-K Chunks (Cosine Distance)

    alt Cosine Distance >= 0.90 (Irrelevant / Out-of-Scope)
        API-->>U: Return fallback message with empty sources []
    else Cosine Distance < 0.90 (Relevant Context Found)
        API->>API: Construct bounded prompt containing Document Excerpts
        API->>LLM: Send System Prompt + Context Excerpts + Query
        LLM-->>API: Return synthesized response
        
        alt LLM indicates missing info ("could not be found", etc.)
            API-->>U: Return fallback message with empty sources []
        else Grounded Answer Generated
            API-->>U: Return Grounded Answer + Source Metadata
        end
    end
```

### Retrieval & Guardrail Mechanics
1. **Document Ingestion & Seeding:** On startup, `rag_service.py` parses `knowledge_base/seed_documents.json` and upserts policies across HR, IT Support, Operations, and Finance into ChromaDB using cosine distance indexing[cite: 1, 2].
2. **Semantic Vector Search:** For incoming questions, ChromaDB executes an approximate nearest neighbor search ($Top\text{-}K = 2$)[cite: 1, 2]. A cosine distance cutoff threshold of $0.90$ filters out weakly correlated context.
3. **Bounded Context Prompting:** Retrieved document chunks are assembled into a structured system prompt that explicitly instructs the model to rely solely on the provided excerpts and avoid external assumptions[cite: 1, 2].
4. **Hallucination Prevention (Unknown Question Handling):** When a user asks a question outside the knowledge base (e.g., *"What is the company maternity leave policy?"*), the pipeline[cite: 1, 2]:
   * Recognizes the knowledge gap via semantic distance or model fallback tokens[cite: 1, 2].
   * Strips ungrounded citation cards (`sources: []`)[cite: 1, 2].
   * Returns a clean fallback response: *"I could not find any policy regarding that in our company knowledge base. Please consult HR or IT directly."*[cite: 1, 2]

---

## 11. Known Limitations

* **Transient Cold Starts (Free Tier):** Render spins down free backend web services after 15 minutes of inactivity, resulting in a 30–45s wake-up latency on initial cold requests.
* **Single-Chunk Document Ingestion:** Long seed documents are currently indexed as single blocks rather than recursive sliding character windows with chunk overlap.
* **Ephemeral Persistence in Cloud Containers:** Free cloud instances do not persist runtime dynamic vector updates across service redeployments unless attached to persistent storage disks or external vector cloud instances.

---

## 12. Potential Future Improvements

1. **Hybrid Search (Dense Vectors + BM25):** Combine dense semantic embeddings with BM25 sparse keyword retrieval via Reciprocal Rank Fusion (RRF) for exact policy error code lookups.
2. **Real-Time Token Streaming:** Implement Server-Sent Events (SSE) or WebSockets on `/api/chat` to stream responses token-by-token for lower perceived latency.
3. **Conversational Multi-Turn Memory:** Add session ID support with sliding-window dialogue history to handle contextual follow-up questions.
4. **Automated Document Ingestion Pipeline:** Create an admin upload dashboard supporting automated PDF, Markdown, and DOCX document parsing and chunking.
