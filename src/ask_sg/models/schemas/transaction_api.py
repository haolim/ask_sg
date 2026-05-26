# Layer 2: API contract (Pydantic)
# Define what goes in and out of our API.
# Pure Pydantic. No DB knowledge

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TransactionResponse(BaseModel):
    id: UUID
    town: str
    block: str
    flat_type: str
    street_name: str
    storey_range: str
    floor_area_sqm: int
    flat_model: str
    lease_commence_year: int
    resale_price: int
    sold_year: int
    sold_month: int
    remaining_lease_year: int
    remaining_lease_month: int
    # Allow Pydantic to read SQLAlchemy ORM objects without needing to manually convert every
    # ORM object to a dictionary first before Pydantic could read it
    # E.g. we can call via our Router (e.g. TransactionResponse.model_validate(orm_object))
    model_config = ConfigDict(
        from_attributes=True
    )

class PaginatedResponse(BaseModel):
    transactions: list[TransactionResponse]
    skip: int
    limit: int
    total: int

