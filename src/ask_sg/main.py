from fastapi import FastAPI
from ask_sg.api.routers import health, transactions, ask

app = FastAPI(title="HDB Resale Transactions API", version="1.0.0")
app.include_router(health.router)
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(ask.router, prefix="/api/v1")
