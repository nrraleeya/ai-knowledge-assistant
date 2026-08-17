# AI Usage & Verification Log

## 1. Tools Used
* **Gemini (Google AI Studio / Gemini 2.5):** Architecture design, RAG grounding prompt engineering, fallback threshold tuning, and system evaluation.
* **Claude Code / GitHub Copilot:** Boilerplate scaffolding for FastAPI endpoints, Pydantic schema validation, Tailwind CSS dark-theme chat UI, and Pytest test fixtures.
* **ChatGPT (OpenAI):** Troubleshooting Windows PowerShell deployment commands, Vercel CLI routing, and Render build error resolution.

---

## 2. AI Contributions

### Example 1: Grounded Synthesis & Anti-Hallucination Prompt Design
AI helped construct and refine the system prompt used in `backend/rag_service.py`[cite: 1, 2]. The design enforces strict context bounding: the LLM is instructed to rely solely on the provided retrieved chunks and to explicitly state when an answer is not present in the text[cite: 1, 2]. This eliminated hallucinated policy details during testing[cite: 1, 2].

### Example 2: Interactive Frontend with Collapsible Citations
AI accelerated frontend development by providing a modular React 18 component structure styled with Tailwind CSS[cite: 1, 2]. It implemented collapsible source citation cards with individual toggle states (`openSources`), animated loading indicators, and error boundary alerts to provide immediate feedback on backend connectivity[cite: 1, 2].

---

## 3. AI Mistake & Engineering Correction
- **Mistake**: When prompted to generate the RAG prompt, the AI coding assistant created an unconstrained prompt template that allowed the model to fallback on its pre-trained general knowledge whenever a document was missing. When queried with *"What is the maternity leave policy?"*, the LLM fabricated a generic 12-week leave policy.
- **Identification**: Caught during automated test execution (`test_unknown_question_avoid_hallucination`), which asserted that out-of-scope queries must return zero sources and an explicit missing-data notice.
- **Correction**: Re-engineered the system prompt to enforce strict bounded answering constraints (*"Answer strictly using ONLY the provided context. If not present, indicate that the policy is not documented."*) and added a pre-generation threshold check returning an immediate fallback when zero chunks pass similarity validation.

---

## 4. Verification Methodology
- **Deterministic Test Verification**: All AI-suggested code was checked with Pytest unit/integration tests.
- **Security & Key Audit**: Verified that no environment variables or hardcoded secrets were placed in frontend source code or committed files.
