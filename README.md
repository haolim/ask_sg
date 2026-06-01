# Ask Singapore (`ask_sg`)

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
- [x] PostgreSQL schema (`resale_transactions`) with the pgvector extension; migrations managed with Alembic
- [x] Bulk ingestion pipeline loading the public HDB resale dataset, with malformed rows logged rather than halting the run
- [x] FastAPI backend — `/health`, `/transactions` (paginated JSON), and `/ask`; interactive docs via Swagger UI at `/docs`
- [x] `/ask` connected to a local LLM (Ollama) returning a streamed response
- [x] Embeddings generated for the dataset and stored in pgvector; top-5 similarity search returns relevant rows for a test question
- [x] Full RAG chain wired into `/ask` — a question retrieves relevant rows and the LLM returns an answer grounded in those rows (orchestrated with Pydantic AI)

## In progress / planned

- [ ] Intent-routing agent — classify a question and route it to RAG or web search (LangGraph)
- [ ] Route the agent through `/ask` with conversation state
- [ ] Evaluation suite — a small golden Q&A set scored for faithfulness and relevancy (RAGAS)
- [ ] Containerisation (Docker) and deployment (Railway backend, Vercel frontend)
- [ ] Web frontend (Next.js)

## Stack

Python · FastAPI · Pydantic · Pydantic AI · SQLAlchemy · Alembic · PostgreSQL · pgvector · Ollama (`nomic-embed-text`)

## Data source

HDB resale flat prices, published as open data by the Singapore government via data.gov.sg.

## Status

Active, in development. This is a self-directed learning project; the checklist above
describes the current state of the repository.
