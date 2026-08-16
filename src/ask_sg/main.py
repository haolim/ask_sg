from fastapi import FastAPI
from ask_sg.api.routers import health, transactions, ask
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HDB Resale Transactions API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(ask.router, prefix="/api/v1")