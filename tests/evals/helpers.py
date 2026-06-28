from ask_sg.agents.deps import AgentDeps
from ask_sg.agents.rag_agent import rag_agent

async def run_pipeline(user_input: str, session, client) -> tuple[str, list[str]]:
    deps = AgentDeps(session=session, client=client)
    result = await rag_agent.run(user_input, deps=deps)
    response = result.output
    contexts = deps.retrieved
    return response, contexts