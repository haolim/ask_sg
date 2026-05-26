# Router Layer 1
# Receives HTTP requests, calls the service, returns HTTP responses.

from fastapi import APIRouter, Depends
from ask_sg.models.schemas.transaction_api import PaginatedResponse
from ask_sg.api.dependencies.db import get_db
from sqlalchemy.orm import Session
from ask_sg.services.resale_transactions import get_resale_transactions

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get("/", response_model=PaginatedResponse)
def get_transactions(skip: int = 0, limit: int= 20, db: Session = Depends(get_db)):
    return get_resale_transactions(
        db=db,
        skip=skip,
        limit=limit
    )