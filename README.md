# Ask Singapore ('ask_sg')

*A self-directed project building a retrieval-augmented generation (RAG) backend over Singapore HDB resale data.*

This is a personal learning project, built to develop hands-on familiarity with the core
components of an AI engineering stack — data ingestion, a typed API layer, local LLM
integration, vector search, and retrieval-augmented generation — by taking one real dataset
(HDB resale transactions, published on data.gov.sg) end to end. It is a work in progress. The checklist below reflects what
currently runs in the repository rather than a finished product.

## What it does

The system answers natural-language questions about Singapore HDB resale transactions. An
incoming question is embedded, matched against stored transaction vectors in PostgreSQL, and
the retrieved rows are passed to a local LLM, which returns an answer grounded in those rows
rather than in the model's own recall.

## Working now

- [x] HDB resale dataset explored and modelled with typed Pydantic schemas
- [x] PostgreSQL schema ('resale_transactions') with the pgvector extension; migrations managed with Alembic
- [x] Bulk ingestion pipeline loading the public HDB resale dataset, with malformed rows logged rather than halting the run
- [x] FastAPI backend — '/health', '/transactions' (paginated JSON), and '/ask'; interactive docs via Swagger UI at '/docs'
- [x] Local LLM via Ollama
- [x] Embeddings generated for the dataset and stored in pgvector; top-5 similarity search returns relevant rows for a test question
- [x] Full RAG chain wired into '/ask' — a question retrieves relevant rows and the LLM returns an answer grounded in those rows (orchestrated with Pydantic AI).
- [x] '/ask' wired to the agents and streamed over Server-Sent-Events (SSE), including lifecycle events ('node_start', 'node_end', 'token', 'error')
- [x] Conversation memory so '/ask' retains context across turns (LangGraph 'MemorySaver' via 'RunnableConfig')
- [x] Route the agent through '/ask' with conversation state
- [x] Evaluation suite — a small golden Q&A set scored for faithfulness and relevancy (RAGAS); also to verify answer grounding
- [x] ngrok tunnel - inference (Ollama) and vector store runs locally
- [x] CI/CD - GitHub Actions runs the RAGAS golden set on every push to main; on passing tests, it deploys to Railway
- [x] Containerisation (Docker) and deployment (Railway backend)
- [x] Web frontend (Next.js) - simple chat UI streaming response from '/ask' via Vercel AI SDK ('useChat')

## In progress / planned
- [ ] Hybrid search - semantic vector search combined with SQL filters (aggregation) and cross-encoder reranking
- [ ] Frontend deployed to Vercel

## Stack

Python · FastAPI · Pydantic · Pydantic AI · LangGraph · SQLAlchemy · Alembic · PostgreSQL · pgvector · Ollama ('nomic-embed-text' embeddings, 'qwen3.5:9b' as model, 'qwen2.5:14b' eval judge) · RAGAS · pytest · Docker · GitHub Actions · Railway · ngrok

## Data source

HDB resale flat prices, published as open data by the Singapore government via data.gov.sg.

## Status

Active, in development. This is a self-directed learning project; the checklist above
describes the current state of the repository.
