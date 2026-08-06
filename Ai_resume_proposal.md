# PRODUCT EXPANSION BLUEPRINT: V2.0

## Phase 1: User Experience & Landing Interface (The "Front Page")
To convert visitors into users, the frontend will be expanded from a simple upload tool into a full landing ecosystem.

* **Hero Section & Value Proposition:** A clean, Neo-Brutalist hero banner explaining the "All-in-One Platform" advantage (Scoring, Roadmap, and Interview Prep in one click).
* **Feature Breakdown (How It Works):** Visual nodes walking the user through the process: 1. Ingestion, 2. AI Semantic Matching, 3. Gap Analysis, 4. Roadmap Generation.
* **The Uniqueness Factor:** A section highlighting our edge—using localized NLP and TF-IDF rather than generic, hallucination-prone generative models for scoring.
* **Support & Redressal:** A dedicated contact modal and bug-reporting ticketing system for users to report broken roadmap links or parsing errors.

## Phase 2: Authentication & State Management
Transitioning from stateless single-use sessions to a persistent user environment.

* **OAuth2 & JWT Integration:** Implementing Google and GitHub login via Auth0 or Firebase Auth.
* **Dashboard & History Tracking:** Once logged in, users will have a private dashboard displaying their past Internship Readiness Index (IRI) scores over time, allowing them to track their upskilling progress.
* **Saved Roadmaps:** Users can bookmark their customized learning roadmaps and check off completed courses (e.g., Udemy, YouTube, arXiv papers).

## Phase 3: Taxonomy Expansion & AI Upgrades
Scaling the NLP engine to handle a wider variety of engineering disciplines and modern tech stacks.

* **Expanded CSE & AIML Frameworks:** Adding extensive spaCy synonym dictionaries for missing modern stacks (e.g., Next.js, LangChain, PyTorch, HuggingFace, Web3/Solidity).
* **Multi-Branch Support:** Expanding the database to score resumes for Electronics & Communication (VLSI, Verilog, IoT) and Mechanical Engineering (AutoCAD, SolidWorks, MATLAB).
* **Contextual Embeddings (Future-Proofing):** Upgrading from standard TF-IDF to a Sentence-Transformer model (like BERT) to understand the context of skills, not just exact keyword matches.
* **AI Mock Interview Simulator:** An interactive module that generates 5 specific technical questions based purely on the skills flagged in the "Needs Work" array.

## Phase 4: Infrastructure & Stability
Bulletproofing the backend to handle multiple authenticated users simultaneously.

* **API-First Aggregation:** Replacing the legacy Python web-scrapers with official YouTube Data v3 and Udemy APIs to completely eliminate "404 Not Found" errors.
* **Redis Caching:** Implementing Redis to cache course links and job description vectors, dropping response times from seconds to milliseconds.

---

## BACKEND API CONTRACTS (For the Engineering Team)
Here are the exact endpoint structures the backend team needs to build in Flask to support the new frontend React components.

### 1. Authentication & User Provisioning
**Endpoint:** `/api/v2/users/auth`
**Method:** `POST`
**Description:** Validates OAuth token and provisions a new user or logs in an existing user.

| Request Payload | Type | Description |
| :--- | :--- | :--- |
| `provider` | String | "google" or "github" |
| `token` | String | OAuth access token |

| Response Output | Type | Description |
| :--- | :--- | :--- |
| `user_id` | UUID | Unique database identifier |
| `session_jwt` | String | Bearer token for protected routes |

### 2. Standardized Resume Analysis (Authenticated)
**Endpoint:** `/api/v2/analyze`
**Method:** `POST`
**Description:** Ingests the resume and JD, scores it, generates the roadmap, and now automatically saves the result to the user's history.

| Request Payload (FormData) | Type | Description |
| :--- | :--- | :--- |
| `resume` | File (PDF) | User's CV document |
| `job_description` | String | Target JD text |
| `target_branch` | String | e.g., "CSE", "AIML", "ECE" |

| Response Output | Type | Description |
| :--- | :--- | :--- |
| `analysis_id` | UUID | ID of this specific analysis |
| `overall_score` | Float | The IRI match percentage |
| `skills_found` | Array | List of "Nailed It" skills |
| `skills_missing` | Array | List of "Needs Work" gaps |
| `roadmap` | Object | The JSON course/paper links |

### 3. Fetch User History
**Endpoint:** `/api/v2/users/{user_id}/history`
**Method:** `GET`
**Description:** Retrieves a chronological list of a user's past resume analyses for the frontend dashboard.

| Request Payload | Type | Description |
| :--- | :--- | :--- |
| `Authorization` | Header | Bearer `{session_jwt}` |

| Response Output | Type | Description |
| :--- | :--- | :--- |
| `history` | Array | List of past scores and dates |
| `trend_delta` | Float | Change in score over time |

### 4. AI Mock Interview Generator
**Endpoint:** `/api/v2/interview/generate`
**Method:** `POST`
**Description:** Takes the `skills_missing` array from a previous analysis and generates targeted interview practice questions.

| Request Payload | Type | Description |
| :--- | :--- | :--- |
| `analysis_id` | UUID | Reference to the previous scan |
| `difficulty` | String | "Beginner", "Intermediate", "Hard" |

| Response Output | Type | Description |
| :--- | :--- | :--- |
| `questions` | Array | 5 targeted technical questions |
| `suggested_answers` | Array | Brief technical talking points |

## Phase 5: Security & Anti-Tampering Hardening
To prevent unauthorized access, score manipulation, and malicious payloads, the platform will implement strict zero-trust backend validation and client-side obfuscation.

* **Client-Side Tamper Prevention (The "Inspect Element" Fix):**
  * **Server-Side Truth:** The frontend UI will be completely "dumb." The IRI score and skill gap match are calculated exclusively on the Python backend. Even if a user changes their score from 34% to 99% using the browser's "Inspect" tab, it will only change visually on their local screen. The backend database and PDF export will still reflect the true 34% score.
  * **Production Obfuscation:** Next.js builds will enforce strict minification and obfuscation. React Developer Tools will be explicitly disabled in the production environment.
  * **HttpOnly JWTs:** Session tokens will be stored in secure, HttpOnly cookies rather than `localStorage` to prevent Cross-Site Scripting (XSS) attacks from stealing user sessions via the browser console.
* **Model & Ingestion Security:**
  * **Anti-Keyword Stuffing (Adversarial Defense):** The TF-IDF engine will enforce strict frequency caps to prevent users from cheating the system by writing "Python" 1,000 times in hidden white text on their PDF.
  * **Immutable Model State:** The Python API layer will have strictly "Read-Only" access to the NLP models and JSON databases. No user input can ever compute, alter, or inject code into the spaCy pipeline.
  * **Malicious File Sanitization:** The PyMuPDF ingestion module will implement strict file-header validation and size limits (e.g., max 5MB) to prevent "PDF bombs" or malicious executable scripts from crashing the container.
* **Infrastructure Protection:**
  * **Strict CORS Policies:** The Flask backend will only accept API requests originating directly from your specific Vercel frontend domain. All other external requests (like Postman or random scripts) will be blocked.
  * **API Rate Limiting:** Endpoints will be capped (e.g., 5 resume uploads per minute per IP address) to prevent DDoS attacks or automated bots from draining server resources.

---

### Additional API Security Specifications

### 5. Security & Rate Limit Middleware
**Middleware:** `validate_and_sanitize()`
**Applied To:** All `/api/v2/*` routes
**Description:** Sits in front of the application logic to strip malicious data before it ever touches the AI models.

| Security Check | Implementation | Consequence of Failure |
| :--- | :--- | :--- |
| **Origin Verification** | Check `Access-Control-Allow-Origin` | Returns `403 Forbidden` |
| **Token Integrity** | Validate JWT signature | Returns `401 Unauthorized` |
| **File Type Validation** | Magic number check (PDFs only) | Returns `415 Unsupported Media Type` |
| **Rate Limit Check** | Redis IP tracker | Returns `429 Too Many Requests` |