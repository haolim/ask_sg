# Router Layer 1
# Receives HTTP requests, calls the service, returns HTTP responses.


from fastapi import APIRouter, Depends
from fastapi.sse import ServerSentEvent, EventSourceResponse
from ask_sg.models.schemas.ask_api import Question, Answer
from ask_sg.services.ask_service import stream_answer
from sqlalchemy.orm import Session
from ask_sg.api.dependencies.db import get_db
from ask_sg.api.dependencies.clients import get_ollama_client
from ollama import Client
from collections.abc import AsyncIterable

router = APIRouter(
    prefix="/ask",
    tags=["Ask"]
)

@router.post("/", response_class=EventSourceResponse)
async def post_question(question: Question, 
                        db: Session = Depends(get_db),
                        client: Client = Depends(get_ollama_client)
                        ) -> AsyncIterable[ServerSentEvent]:
        try:
            async for event_dict in stream_answer(question=question.question, db=db, client=client):
                # Take a shallow copy of the data to prevent mutation
                payload = event_dict.copy()
                # Remove the type from the paylod and assign to a variable
                event_type = payload.pop("type")
                # Yield it and let frontend decide the event type it wants to consume
                yield ServerSentEvent(
                    data=payload,
                    event=event_type
                )
        except Exception as e:
            yield ServerSentEvent(
                data={"text": str(e)},
                event="error"
            )