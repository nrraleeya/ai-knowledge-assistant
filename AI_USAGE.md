# AI Usage & Verification Log

## 1. Tools Used
- **Gemini / Claude Code**: Architecture design, Pydantic schema validation, and Pytest test mock creation.
- **GitHub Copilot**: Autocompleting boilerplate FastAPI routes and Tailwind CSS styling templates.

## 2. AI Contributions
- **Automated Mock Test Suite Architecture**: AI generated the Pytest fixtures and mock decorators for `unittest.mock.patch`, allowing complete RAG and API test execution in under 0.8 seconds without incurring live Gemini API quota costs.
- **Vector Distance Filtering Logic**: AI proposed the cosine similarity threshold cutoff logic (< 0.70) within the ChromaDB query pipeline to separate weak/unrelated vector matches from relevant policy documents.

## 3. AI Mistake & Engineering Correction
- **Mistake**: When prompted to generate the RAG prompt, the AI coding assistant created an unconstrained prompt template that allowed the model to fallback on its pre-trained general knowledge whenever a document was missing. When queried with *"What is the maternity leave policy?"*, the LLM fabricated a generic 12-week leave policy.
- **Identification**: Caught during automated test execution (`test_unknown_question_avoid_hallucination`), which asserted that out-of-scope queries must return zero sources and an explicit missing-data notice.
- **Correction**: Re-engineered the system prompt to enforce strict bounded answering constraints (*"Answer strictly using ONLY the provided context. If not present, indicate that the policy is not documented."*) and added a pre-generation threshold check returning an immediate fallback when zero chunks pass similarity validation.

## 4. Verification Methodology
- **Deterministic Test Verification**: All AI-suggested code was checked with Pytest unit/integration tests and static typing validation (`mypy` / Pydantic).
- **Security & Key Audit**: Verified that no environment variables or hardcoded secrets were placed in frontend source code or committed files.