# Services Layer 4
# Business logic lives here.
# Talks to the Repository.
# Never touches HTTP or raw SQL

from ollama import Client
from ask_sg.agents.agent import agent
from ask_sg.agents.deps import AgentDeps
from sqlalchemy.orm import Session


async def get_answer(question: str,
               db: Session,
               client: Client
               ) -> str:
    result = await agent.run(
        user_prompt=question,
        deps=AgentDeps(session = db, client = client)
    )
    return result.output
