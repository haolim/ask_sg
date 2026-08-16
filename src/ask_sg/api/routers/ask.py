# Router Layer 1
# Receives HTTP requests, calls the service, returns HTTP responses.


from fastapi import APIRouter, Depends, Header, Response
from fastapi.sse import ServerSentEvent, EventSourceResponse
from ask_sg.services.ask_service import stream_answer
from sqlalchemy.orm import Session
from ask_sg.api.dependencies.db import get_db
from ask_sg.api.dependencies.clients import get_ollama_client
from ollama import Client
from typing import AsyncIterable
from uuid import uuid4
import traceback
from pydantic import BaseModel

class UIPart(BaseModel):
    type: str
    text: str | None = None

class UIMessage(BaseModel):
    role: str
    parts: list[UIPart]

class ChatRequest(BaseModel):
    messages: list[UIMessage]

router = APIRouter(
    prefix="/ask",
    tags=["Ask"]
)

@router.post("/", response_class=EventSourceResponse)
async def post_question(response: Response,
                        #question: Question,
                        payload: ChatRequest,
                        db: Session = Depends(get_db),
                        client: Client = Depends(get_ollama_client),
                        session_id: str = Header(default=None)
                        ) -> AsyncIterable[ServerSentEvent]:

        question_text = payload.messages[-1].parts[-1].text


        thread_id = session_id or str(uuid4())
        response.headers["x-vercel-ai-ui-message-stream"] = "v1"
        try:
            yield ServerSentEvent(
                 data={"type": "text-start", "id": thread_id}
            )
            async for event_dict in stream_answer(question=question_text, db=db, client=client, thread_id=thread_id):
                # Remove the type from the paylod and assign to a variable
                event_type = event_dict["type"]
                # Yield it and let frontend decide the event type it wants to consume
                if event_type == "token":
                    yield ServerSentEvent(
                        data={"type": "text-delta", "id": thread_id, "delta": event_dict["text"]},
                    )

            yield ServerSentEvent(
                 data={"type": "text-end", "id": thread_id}
            )    
        except Exception as e:
            traceback.print_exc()
            yield ServerSentEvent(
                data={"type": "error", "errorText": str(e)},
            )