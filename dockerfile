FROM python:3.14.6-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . .
RUN uv sync --frozen --no-dev

FROM python:3.14.6-slim AS runtime
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "ask_sg.main:app", "--host", "0.0.0.0", "--port", "8000"]