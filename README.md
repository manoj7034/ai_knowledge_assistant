Project: Enterprise AI Knowledge Platform

Project Goal

Build an enterprise platform where users can:

Upload company documents
Ask natural language questions
Get grounded answers with citations
Use AI agents to decide when to retrieve documents or invoke tools
Use a custom MCP server for enterprise integrations
Evaluate answer quality automatically using RAGAS
Monitor retrieval quality and latency

Final Architecture

                     React (Future)
                          │
                    FastAPI Backend
                          │
                  JWT Authentication
                          │
                 LangGraph Supervisor
                          │
     ┌────────────────────┼─────────────────────┐
     │                    │                     │
Retrieval Agent      Tool Agent         Evaluation Agent
     │                    │                     │
     │                    │                     │
 Vector DB          Custom MCP          RAGAS / DeepEval
     │                    │                     │
 Document Store      PostgreSQL         Evaluation DB
     │                    │
     └──────────── AWS Bedrock ────────────────┘

Tech Stack

| Layer          | Technology                |
| -------------- | ------------------------- |
| Backend        | FastAPI                   |
| Authentication | JWT                       |
| ORM            | SQLAlchemy 2.0            |
| Database       | PostgreSQL                |
| Vector DB      | Weaviate (or Qdrant)      |
| LLM            | AWS Bedrock (Claude/Nova) |
| Framework      | LangGraph                 |
| RAG            | LangChain                 |
| Evaluation     | RAGAS + DeepEval          |
| Storage        | AWS S3                    |
| Agent Tools    | Custom MCP Server         |
| Deployment     | Docker                    |
| Monitoring     | LangSmith + Prometheus    |
| Cache          | Redis (later)             |


Development Phases

Phase 1 — Backend Foundation

Goal: Build a production-ready FastAPI application.

Features:

Project structure
Logging
Configuration
JWT Authentication
PostgreSQL
SQLAlchemy
Alembic
Docker
Health API

Deliverable:

enterprise-ai-platform/

app/
    api/
    core/
    models/
    schemas/
    database/
    services/
    utils/

tests/

Dockerfile

docker-compose.yml

Phase 2 — Knowledge Base

Build document ingestion.

Upload PDF

↓

S3

↓

Parser

↓

Chunker

↓

Embedding

↓

Vector DB

Supported:
- PDF
- DOCX
- TXT
- Markdown

Later:
- Excel
- CSV

Phase 3 — Retrieval

User Question

↓

Query Rewriting

↓

Hybrid Search

↓

Reranker

↓

Top-k Documents

↓

LLM

Learn:

Dense Retrieval
BM25
Hybrid Search
Metadata Filtering
Parent Retriever
Multi Query Retrieval

Phase 4 — LangGraph

Phase 5 — Custom MCP

Example Tools:

search_documents()

search_database()

document_summary()

employee_lookup()

ticket_lookup()

weather()

calculator()

company_policy()

vector_search()

Phase 6 — Evaluation

Automatic evaluation

Question

↓

Answer

↓

Ground Truth

↓

RAGAS

↓

Store Metrics


Metrics:
Faithfulness
Context Recall
Context Precision
Answer Relevancy
Semantic Similarity

Phase 7 — Observability

Track:
Latency

Embedding Time

Retrieval Time

Generation Time

LLM Tokens

Costs

RAGAS Score

Hallucination %

Tool Calls

Phase 8 — Production

Add

Streaming
Async
Redis
Docker
AWS Deployment
CI/CD
Background Workers

AWS Services:

| Service         | Purpose          |
| --------------- | ---------------- |
| Bedrock         | LLM inference    |
| S3              | Document storage |
| IAM             | Permissions      |
| CloudWatch      | Logs             |
| ECS (optional)  | Deployment       |
| Secrets Manager | API keys         |
| ECR             | Docker images    |


Folder Strcuture:

enterprise-ai-platform/

backend/

    app/

        api/
        auth/
        core/
        db/
        models/
        schemas/
        services/
        repositories/

        rag/

            loaders/
            chunkers/
            embeddings/
            retrievers/
            rerankers/

        agents/

            graph/
            nodes/
            tools/

        evaluation/

            ragas/
            deepeval/

        mcp/

            server/
            client/
            tools/

        observability/

        utils/

frontend/

docker/

terraform/

tests/

docs/