# Services Layer 4
# Business logic lives here.
# Talks to the Repository.
# Never touches HTTP or raw SQL

# total_duration: how long the response took to generate (in nanoseconds * 10^9 - /s)
# load_duration: how long the model took to load (in nanoseconds * 10^9 - /s)
# prompt_eval_count: how many input tokens were processed
# prompt_eval_duration: how long it took to evaluate the prompt (in nanoseconds * 10^9 - /s)
# eval_count: how many output tokens were processed
# eval_duration: how long it took to generate the output tokens (in nanoseconds * 10^9 - /s)

# response = requests.get("http://localhost:11434/api/tags")
# print(json.dumps(response.json(), indent=2))


from anthropic import Anthropic
from ollama import ResponseError

model = "gemma4:e2b"
max_tokens = 1024

client = Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama"
)
def get_answer(question: str):
    try:
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system="Do not use LaTeX or mathematical notation, plain text only.",
            messages=[{
                'role': 'user', 'content': question
            }]
        ) as stream:
            for text in stream.text_stream:
                yield text
    except ResponseError as e:
        raise e

