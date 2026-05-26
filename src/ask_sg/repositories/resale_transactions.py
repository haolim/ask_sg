# Repositories Layer 5
# All DB queries live here.
# Talks to ORM.
# No business logic, no HTTP


from sqlalchemy.orm import Session
from ask_sg.models.orm.resale_transactions import ResaleTransactions

def get_transactions(db: Session, skip: int, limit: int):
    return db.query(ResaleTransactions).offset(skip).limit(limit).all()


def get_total_count(db: Session) -> int:
    return db.query(ResaleTransactions).count()