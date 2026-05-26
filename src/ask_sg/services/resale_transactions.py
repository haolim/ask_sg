# Services Layer 4
# Business logic lives here.
# Talks to the Repository.
# Never touches HTTP or raw SQL

from ask_sg.models.schemas.transaction_api import TransactionResponse, PaginatedResponse
from ask_sg.repositories import resale_transactions as transactions_repo
from sqlalchemy.orm import Session

def get_resale_transactions(db: Session, skip: int, limit: int) -> PaginatedResponse:
    total_count = transactions_repo.get_total_count(db)
    transactions = transactions_repo.get_transactions(db, skip, limit)
    return PaginatedResponse(
        transactions=transactions, 
        skip=skip, 
        limit=limit, 
        total=total_count
        )