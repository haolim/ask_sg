# Router Layer 1
# Receives HTTP requests, calls the service, returns HTTP responses.


from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ask_sg.models.schemas.ask_api import Question, Answer
from ask_sg.services.ask_service import get_answer

router = APIRouter(
    prefix="/ask",
    tags=["Ask"]
)

@router.post("/", response_class=StreamingResponse)
def post_question(question: Question):
    return StreamingResponse(
        get_answer(question.question),
        media_type="text/plain"
        )