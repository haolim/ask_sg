# Running ask_sg with Docker

The stack (FastAPI + PostgreSQL/pgvector) runs via Docker Compose. 

Ollama runs on the **host** (not in a container) and is reached from the containers at 'host.docker.internal'.

## Prerequisites

- Docker Desktop
- [Ollama](https://ollama.com) running on the host.

Pull the models used by the stack:
- Embedding Model: `nomic-embed-text`
- LLM Judge: `qwen2.5:14b`
- Agent: `qwen3.5:9b`

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:14b
ollama pull qwen3.5:9b
```

Image is published on Docker Hub. 

To pull image directly:

```bash
docker pull hipythea/ask_sg:0.1.0
```

Else, to use the pre-built image, in `docker-compose.yml`, update services to reference:
```yaml
image: hipythea/ask_sg:0.1.0
```

Then use the command `docker compose up` to pull the image

## 1. Configure environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

For a Docker setup use Docker section:

```dotenv
DATABASE_URL=postgresql+psycopg2://user:password@db:5432/ask_sg
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_EMBEDDING_MODEL_BASE_URL=http://host.docker.internal:11434
```

- `db` is the service name that resolves to the database
- `host.docker.internal` resolves to the host machine, where Ollama is running.

## 2. Start the container

```bash
docker compose up --build
```

The API is then available at `http://localhost:8000`.
Docs at `http://localhost:8000/docs`.

## 3. Load data

In the docker-compose.yml service, the ingest jobs needs to be run on demand:

```bash
docker compose run --rm ingest
```

This will load the dataset from `data/raw`

## 4. Generate embeddings

After ingest, generate the vector embeddings using the `generate_embeddings.py` script in the /ask_sg/scripts folder:

```bash
docker compose run --rm api python -m ask_sg.scripts.generate_embeddings
```

This may take ~2-3 hours (at least on my local hardware). If it gets interrupted, the next run will process rows without an existing embedding, allowing the run to resume.

## 5. Try it

Once the container has started, give it a try at `http://localhost:8000/docs`. Or you can use curl via the command line (with example question):

```bash
curl.exe -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are some recent 4-room flat transactions in Tampines?"}'
```

## Shutting down

Use the following commands to shut down the container and keep the volume:
```bash
docker compose down
```

If you want to delete everything, use the following command:
```bash
docker compose down -v
```