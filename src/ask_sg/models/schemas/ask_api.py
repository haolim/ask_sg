# Layer 2: API contract (Pydantic)
# Define what goes in and out of our API.
# Pure Pydantic. No DB knowledge
from pydantic import BaseModel

class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str