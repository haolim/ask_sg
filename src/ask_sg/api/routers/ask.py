# Router Layer 1
# Receives HTTP requests, calls the service, returns HTTP responses.


from fastapi import APIRouter, Depends
from ask_sg.models.schemas.ask_api import Question, Answer
from ask_sg.services.ask_service import get_answer
from sqlalchemy.orm import Session
from ask_sg.api.dependencies.db import get_db
from ask_sg.api.dependencies.clients import get_ollama_client
from ollama import Client

router = APIRouter(
    prefix="/ask",
    tags=["Ask"]
)

@router.post("/")
async def post_question(question: Question, 
                        db: Session = Depends(get_db),
                        client: Client = Depends(get_ollama_client)
                        ):
    return await get_answer(question.question, db = db, client = client)