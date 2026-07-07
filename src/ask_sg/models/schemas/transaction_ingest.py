from pydantic import BaseModel, field_validator, Field, model_validator
import calendar

# 1. PYDANTIC MODEL - Validation layer
class HDBResaleTransaction(BaseModel):
    town: str
    flat_type: str
    block: str
    street_name: str
    storey_range: str
    floor_area_sqm: int = Field(gt=0, description="Floor Area in SQM")
    flat_model: str
    lease_commence_year: int
    resale_price: int = Field(gt=0, description="Transacted price in SGD")
    sold_year: int = Field(description="Sold year")
    sold_month: int = Field(description="Sold month")
    remaining_lease_year: int = Field(description="Remaining lease - Year part")
    remaining_lease_month: int = Field(description="Remaining lease - Month part")
    embedding_text: str | None = None

    @field_validator('floor_area_sqm', 'resale_price', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        if v is not None:
            return int(float(v))
        return v

    @field_validator('sold_month')
    @classmethod
    def sold_month_must_be_between_1_and_12(cls, v):
        if v < 1 or v > 12:
            raise ValueError(f'invalid month detected: {v}')
        return v
    
    # Check remaining lease month value - if 12 then the year should be incremented
    @field_validator('remaining_lease_month')
    @classmethod
    def remaining_lease_month_must_be_between_0_and_11(cls, v):
        if v < 0 or v > 11:
            raise ValueError(f'invalid remaining lease month detected: {v}')
        return v


    @field_validator('remaining_lease_year')
    @classmethod
    def remaining_lease_year_must_be_valid(cls, v):
        if v > 99:
            raise ValueError(f'invalid remaining lease detected: {v}')
        return v
    
    def to_embedding_text(self) -> str:
        month_name = calendar.month_name[self.sold_month]
        return (
            f"{self.flat_type} flat located in {self.town} town, "
            f"at street {self.street_name} and block {self.block}. "
            f"The flat model is {self.flat_model}. "
            f"Floor area is {self.floor_area_sqm} sqm. "
            f"Storey range: {self.storey_range}. "
            f"Sold in {month_name} {self.sold_year} for S${self.resale_price:,}. "
            f"Lease commenced in {self.lease_commence_year}. "
            f"Remaining lease: {self.remaining_lease_year} years {self.remaining_lease_month} months."
        )
    
    @model_validator(mode='after')
    def set_embedding_text(self):
        self.embedding_text = self.to_embedding_text()
        return self