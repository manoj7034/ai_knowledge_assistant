# Bruhaspathi — Enterprise AI Knowledge Platform

Bruhaspathi is a production-ready Enterprise AI Knowledge Assistant and RAG (Retrieval-Augmented Generation) platform written in Python. It empowers organizations to ingest multi-format documents, perform multi-tenant hybrid search, and generate strictly grounded, hallucination-resistant answers with citations.

---

## 🏛️ System Architecture

```
                                [ Client / React Frontend ]
                                             │
                                             ▼
                              [ FastAPI Gateway (REST API) ]
                                             │
                        ┌────────────────────┴────────────────────┐
                        ▼                                         ▼
             [ JWT Authentication ]                     [ Multi-Tenant Context ]
         (Access & DB Refresh Tokens)                    (Owner ID / RBAC Filters)
                        │                                         │
       ┌────────────────┴────────────────┐                        │
       ▼                                 ▼                        │
[ Document Ingestion Pipeline ]    [ Hybrid Search & RAG Pipeline ]◄──────┘
  • Multi-Format Parsers             • Dense Vector Search (Weaviate)
    (PDF / DOCX / TXT)               • BM25 Sparse Keyword Search (Weaviate)
  • Chunking Engine                  • Reciprocal Rank Fusion (RRF k=60)
    (Semantic / Recursive / Layout)  • Cross-Encoder Reranking (ms-marco-MiniLM)
  • Embeddings (bge-small-en-v1.5)   • Context Compression (Thresholding)
  • Storage (Local / S3)             • Grounded Prompt Construction
  • Dual Storage:                    • LLM Inference (Gemini / Ollama / Bedrock)
    PostgreSQL + Weaviate            • Grounded Response + Source Citations
```

---

## 🚀 Tech Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | Async REST API, Pydantic v2 settings, Dependency Injection |
| **Authentication** | JWT + PostgreSQL | HS256 Access Tokens + Revocable DB-backed Refresh Tokens |
| **Relational Database** | PostgreSQL + SQLAlchemy 2.0 | Schema: `enterprise_ai`, UUID PKs, Alembic migrations |
| **Vector Database** | Weaviate v4 | Self-provided vectors, HNSW index, BM25 keyword index |
| **Embeddings** | Sentence-Transformers | `BAAI/bge-small-en-v1.5` (L2 Normalized, 384-dim) |
| **Re-ranker** | Cross-Encoder | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| **LLM Providers** | Google Gemini / Ollama | `google-genai` SDK & local Ollama models |
| **Document Parsers** | PyMuPDF, python-docx | PDF, DOCX, TXT extraction |
| **Orchestration / Agents** | LangGraph *(In Progress)* | Multi-agent Supervisor, Tool Agent, Evaluation Agent |
| **Tool Protocol** | Custom MCP Server *(Planned)* | Model Context Protocol for enterprise tool execution |
| **Evaluation** | RAGAS / DeepEval *(Planned)* | Faithfulness, Context Recall, Precision, Answer Relevancy |
| **Containerization** | Docker & Docker Compose | Weaviate vector engine, PostgreSQL |

---

## 📂 Project Structure

```text
Bruhaspathi/
├── backend/
│   ├── alembic/                      # Database migrations
│   │   ├── versions/                 # Version migration scripts
│   │   └── env.py
│   ├── app/
│   │   ├── api/                      # API routing
│   │   │   └── v1/                   # v1 endpoints (auth, users, documents, search, chat)
│   │   ├── auth/                     # JWT tokens, security, hashing, auth services
│   │   ├── chunking/                 # Semantic, Recursive, Layout-aware chunking
│   │   ├── compression/              # Retrieval context compression
│   │   ├── config/                   # Settings & configuration management
│   │   ├── core/                     # Lifespan app state, structured logging
│   │   ├── database/                 # SQLAlchemy engine, session, declarative base
│   │   ├── dependencies/             # FastAPI dependency injections
│   │   ├── embeddings/               # Local BGE embedding provider & factory
│   │   ├── exceptions/               # Custom domain exceptions and HTTP handlers
│   │   ├── extractors/               # File parsers (PDF, DOCX, TXT)
│   │   ├── llms/                     # LLM providers (Gemini, Ollama) and factory
│   │   ├── models/                   # SQLAlchemy ORM models (User, Document, DocumentChunk)
│   │   ├── prompts/                  # Grounded prompt templates
│   │   ├── rag/                      # ContextBuilder, RAGPromptBuilder, RAGService
│   │   ├── repositories/             # Data access layer (User, Document, Chunk repos)
│   │   ├── rerankers/                # Cross-Encoder re-ranking service
│   │   ├── retrieval/                # Reciprocal Rank Fusion (RRF) algorithm
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── scripts/                  # Standalone test & validation scripts
│   │   ├── services/                 # Business logic (Document, Search, Chat services)
│   │   ├── storage/                  # Local & S3 file storage providers
│   │   ├── vectorstores/             # Weaviate client and collection management
│   │   └── main.py                   # FastAPI application factory & lifespan
│   ├── tests/                        # Pytest suite for auth, ingestion, RAG
│   ├── alembic.ini                   # Alembic configuration
│   └── Dockerfile
├── docker-compose.yml                # Multi-container services (Weaviate)
├── pyproject.toml                    # Python project dependencies & metadata
└── README.md                         # Project documentation
```

---

## ⚡ Implemented Features & Pipelines

### 1. Authentication & Multi-Tenancy
- **JWT Authentication**: Passwords hashed with `bcrypt` (work factor 12).
- **Token Rotation**: Short-lived access tokens (`30m`) and database-persisted refresh tokens (`7d`) with revocation support on logout.
- **Tenant Isolation**: All documents, chunks, vector embeddings, and search queries are strictly filtered by `owner_id`.

### 2. Document Processing & Ingestion Pipeline
1. **Upload**: Receives file via `POST /api/v1/documents/upload`.
2. **Storage**: Persists raw file to local storage or S3 with a unique UUID filename.
3. **Text Extraction**:
   - **PDF**: PyMuPDF (`fitz`) page-by-page text extraction.
   - **DOCX**: `python-docx` paragraph extractor.
   - **TXT**: Raw UTF-8 decoding.
4. **Intelligent Chunking** ([`ChunkerFactory`](backend/app/chunking/factory.py)):
   - **Semantic Chunking**: Splits text into sentences, embeds them with BGE, computes adjacent cosine similarity, and splits at topical boundaries (`SEMANTIC_CHUNK_THRESHOLD = 0.70`).
   - **Recursive Chunking**: Configurable size (`1000`) and overlap (`200`).
   - **Layout-Aware Chunking**: Preserves headers, sections, and formatting.
5. **Relational Persistence**: Chunks stored in PostgreSQL (`document_chunks` table).
6. **Vector Indexing**: Generates dense embeddings using `BAAI/bge-small-en-v1.5` and batch indexes into Weaviate with metadata.

### 3. Multi-Stage Hybrid Retrieval Pipeline
1. **Dense Semantic Search**: Top-10 near-vector similarity search in Weaviate.
2. **Sparse Keyword Search**: Top-10 BM25 search in Weaviate over document text.
3. **Reciprocal Rank Fusion (RRF)**: Combines dense and sparse ranked lists using:
   $$\text{RRF Score} = \sum_{m \in M} \frac{1}{k + \text{rank}_m(d)} \quad (k=60)$$
4. **Cross-Encoder Re-ranking**: Scores query-document pairs with `cross-encoder/ms-marco-MiniLM-L-6-v2` for precise semantic alignment.
5. **Context Compression**: Filters out low-confidence chunks based on `RERANK_SCORE_THRESHOLD`.

### 4. Grounded RAG & Generation
- **Context Builder**: Assembles structured markdown contexts with source metadata tags (`[Source N: filename, chunk_index]`).
- **Hallucination Prevention**: Strict system prompts enforcing answers strictly based on retrieved documents, returning a polite fallback if the context is insufficient.
- **LLM Integrations**: Pluggable support for **Google Gemini** (`gemini-2.5-flash` / `gemini-1.5-pro`) and local **Ollama** models.

---

## 📡 API Endpoints

### Health
- `GET /health` — Service health check.

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/register` — Register a new user.
- `POST /api/v1/auth/login` — Login and receive JWT access + refresh tokens.
- `POST /api/v1/auth/refresh` — Rotate refresh token and get a new access token.
- `POST /api/v1/auth/logout` — Revoke refresh token and invalidate session.

### Documents (`/api/v1/documents`)
- `POST /api/v1/documents/upload` — Upload and trigger document processing.
- `GET /api/v1/documents` — List all documents belonging to the authenticated user.
- `GET /api/v1/documents/{document_id}` — Get document metadata and processing status.
- `DELETE /api/v1/documents/{document_id}` — Delete document and associated chunks/vectors.

### Search & Chat (`/api/v1`)
- `GET /api/v1/search?query=...` — Execute full multi-stage hybrid search (returns semantic, keyword, fusion, reranked, and compressed results).
- `POST /api/v1/chat` — Ask natural language questions; returns grounded answer with source citations.

---

## 🛠️ Environment Configuration (`.env`)

```ini
APP_NAME="Enterprise AI Platform"
APP_VERSION="0.1.0"
APP_ENV="development"
DEBUG=True

# Database (PostgreSQL)
DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/enterprise_ai_db"
DB_SCHEMA="enterprise_ai"

# Security / JWT
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# File Storage
STORAGE_PROVIDER="local"
STORAGE_PATH="storage"
LOCAL_STORAGE_PATH="./storage"

# Chunking & Embeddings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
CHUNKING_STRATEGY="semantic"
SEMANTIC_CHUNK_THRESHOLD=0.70
EMBEDDING_PROVIDER="local"
EMBEDDING_MODEL="BAAI/bge-small-en-v1.5"

# Vector Store (Weaviate)
WEAVIATE_HOST="localhost"
WEAVIATE_HTTP_PORT=8080
WEAVIATE_GRPC_PORT=50051
WEAVIATE_COLLECTION="DocumentChunks"

# Retrieval & Reranking
SEMANTIC_TOP_K=10
BM25_TOP_K=10
RRF_TOP_K=10
RERANK_TOP_K=5
RERANK_SCORE_THRESHOLD=0.0

# LLM Configuration
LLM_PROVIDER="gemini" # or "ollama"
LLM_MODEL="gemini-2.5-flash"
GEMINI_API_KEY="your-gemini-api-key"
```

---

## 🚦 Getting Started

### 1. Start Vector Database
```bash
docker-compose up -d
```

### 2. Install Dependencies
Using `uv` (recommended) or standard `pip`:
```bash
uv sync
# or
pip install -e .
```

### 3. Run Database Migrations
```bash
cd backend
alembic upgrade head
```

### 4. Start the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API documentation will be available at: `http://localhost:8000/docs`.

### 5. Running Tests
```bash
pytest backend/tests
```

---

## 🗺️ Project Roadmap & Status

- [x] **Phase 1: Backend Foundation** (FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, JWT Auth, Multi-tenancy)
- [x] **Phase 2: Knowledge Ingestion** (PDF/DOCX/TXT parsers, Semantic & Recursive chunking, BGE embeddings, Weaviate indexing)
- [x] **Phase 3: Hybrid Retrieval** (Dense + BM25, Reciprocal Rank Fusion, Cross-Encoder reranking, Context compression)
- [x] **Phase 4: RAG Engine** (Grounded prompt builder, Gemini & Ollama integration, Source citations)
- [ ] **Phase 5: Agentic LangGraph & MCP** (Supervisor Agent, Retrieval & Tool Agents, Custom Model Context Protocol server)
- [ ] **Phase 6: Automated Evaluation** (RAGAS / DeepEval automated faithfulness, precision, recall benchmarks)
- [ ] **Phase 7: Observability & Production** (Streaming SSE, Prometheus/LangSmith monitoring, Redis cache, AWS deployment)
- [ ] **Phase 8: Frontend** (Modern React + Vite interactive chat & document dashboard)