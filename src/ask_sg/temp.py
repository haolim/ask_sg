# @app.get("/")
# def root():
#     return {"message": "Hello Bigger Application"}

#app.include_router(accounts.router, prefix="/api/v1")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
# )

# # Current messy state — your job is to unify this
# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     price = Column(Float)
#     internal_cost = Column(Float)  # should NOT appear in API response

# class ProductCreate(BaseModel):
#     title: str
#     price: float
#     internal_cost: float

# class ProductResponse(BaseModel):
#     id: int
#     title: str
#     price: float
#     model_config = {"from_attributes": True}

# fake_users_db: dict[int, dict] = {
#     1: {"userId": 1, "name": "Mr A"},
#     2: {"userId": 2, "name": "Mr B"},
#     4: {"userId": 4, "name": "Mr D"},
#     5: {"userId": 5, "name": "Mr E"},
#     6: {"userId": 6, "name": "Mr F"}
# }

# fake_users_db2: dict[int, str] = {1: "Mr A", 2: "Mr B"}

# class User(BaseModel):
#     userId: int
#     name: str

# @app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
# def create_user(user: User):
#     validate_name(user.name)
#     return user


# @app.get("/products/{product_id}")
# def get_product(
#     product_id: Annotated[int, Path(gt=0, title="The ID to get")],
#     currency: str = Query(default="USD"),
#     limit: int = Query(default=10, ge=1, le=50)
#     ):
#     return {"product_id": product_id, "currency": currency, "limit": limit}

# def validate_name(name: str) -> None:
#     if name is None or name.strip() == "":
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Name can't be empty string or whitespace"
#         )

# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: User) -> dict:
#     if user_id not in fake_users_db2:
#         raise HTTPException(
#             status_code = status.HTTP_404_NOT_FOUND,
#             detail = "User not found"
#         )
#     return {"message": f"User {user_id} updated successfully"}

# @app.delete("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
# def delete_user(user_id: int):
#     if user_id not in fake_users_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     if user_id == 1:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail = "Cannot delete admin user"
#         )
#     return {"message": f"User {user_id} deleted successfully"}

# @app.get("/user/{userId}", response_model=User, status_code=200)
# def get_user(userId: int):
#     if userId not in fake_users_db2:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail = "User not found."
#         )
#     return {"userId": userId, "name": fake_users_db2[userId]}

# class Product(BaseModel):
#     name: str
#     price: float = Field(ge=0)
#     tags: list[str] = []

# class ProductInternal(Product):
#     cost_price: float = Field(ge=0)
    

# @app.post(
#         "/product/", 
#         response_model=Product, 
#         response_model_exclude_unset=True,
#         status_code=status.HTTP_201_CREATED
#         )
# def create_product(product: ProductInternal):
#     return product.model_dump(exclude_unset=True)


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# fake_items_db = [{"item_name": "Foo"}, 
#                  {"item_name": "Bar"}, 
#                  {"item_name": "Baz"},
#                  {"item_name": "a"}, 
#                  {"item_name": "b"}, 
#                  {"item_name": "c"},
#                  {"item_name": "d"}, 
#                  {"item_name": "e"}, 
#                  {"item_name": "f"},
#                  {"item_name": "g"}, 
#                  {"item_name": "h"}, 
#                  {"item_name": "i"},
#                  {"item_name": "j"}, 
#                  {"item_name": "k"}, 
#                  {"item_name": "l"},
#                  {"item_name": "m"}, 
#                  {"item_name": "n"}, 
#                  {"item_name": "o"},
#                  {"item_name": "p"}, 
#                  {"item_name": "q"}, 
#                  {"item_name": "r"},
#                  {"item_name": "s"}, 
#                  {"item_name": "t"}, 
#                  {"item_name": "u"},
#                  {"item_name": "v"}, 
#                  {"item_name": "w"}, 
#                  {"item_name": "x"}
#                  ]

# @app.post("/item/")
# def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# @app.get("/models/{model_name}")
# def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning!"}
#     if model_name is ModelName.resnet:
#         return {"model_name": model_name, "message": "LeCNN all the iamges!"}
    
#     return {"model_name": model_name, "message": "Have some residuals"}

# @app.get("/transactions/")
# def read_transaction(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

# @app.get("/users/{user_id}/items/{item_id}")
# def read_user_item(user_id: int, 
#                    item_id: str,
#                     q: str | None = None, 
#                    short: bool = False):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description."}
#         )
#     return item


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result





# import random
# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     ollama_base_url: str
#     env: str = "production"
#     tavily_api_key: str

#     model_config = SettingsConfigDict(
#         env_file = ".env",
#         env_file_encoding= "utf-8",
#         case_sensitive = False,
#         extra = "ignore"
#     )

# settings = Settings()

# from ask_sg.scripts.generate_embeddings import embed_text
# from ollama import Client
# from ask_sg.core.database import SessionLocal
# from sqlalchemy import select
# from ask_sg.models.orm.resale_transactions import ResaleTransactions
# from ask_sg.models.orm.resale_transactions_embeddings import ResaleTransactionsEmbeddings
# client = Client()
# question = "what are some year 2025 4-room transactions in Tampines? Just give me the town, sold year and price sold."



# session = SessionLocal()
# OLLAMA_MODEL = "nomic-embed-text"

# try:
#     """Embed the question and find the top-k most similar transactions."""
#     query_vector = embed_text(client, question)
#     distance = ResaleTransactionsEmbeddings.embedding.cosine_distance(query_vector).label("distance")
#     stmt = (
#         select(
#                 # ResaleTransactions.embedding_text,
#                 ResaleTransactions.town,
#                 ResaleTransactions.flat_type,
#                 ResaleTransactions.floor_area_sqm,
#                 ResaleTransactions.resale_price,
#                 ResaleTransactions.sold_year,
#                 distance,
#                 #ResaleTransactionsEmbeddings.embedding.cosine_distance(query_vector).label('distance'),
#             )
#             .join(
#                 ResaleTransactionsEmbeddings,
#                 ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id
#             )
#             .where(
#                 ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL
#             )
#             .order_by(distance)
#             .limit(100)
#     )
#     results = session.execute(stmt)
#     rows = results.all()
    # print(f"\nQuestion: {question}")
    # print(f"{'Town':<15} {'Type':<12} {'Sqm':<6} {'Price':<12} {'Year':<6} {'Flat Model':<18} {'Dist':<8}")
    # print("-" * 90)
    # for row in results:
    #     print(f"{row.town:<15} {row.flat_type:<12} {row.floor_area_sqm:<6} "
    #         f"${row.resale_price:>10,} {row.sold_year:<6} {row.flat_model:<18} {row.distance: .4f}")

    
    # print(rows)
#     context = "\n".join(
#         # f"{r.embedding_text}"
#         f"{r.town}, {r.flat_type}, floor size of {r.floor_area_sqm} sqm, "
#         f"sold at a price of ${r.resale_price:,}, "
#         f"sold in the year:{r.sold_year}"
#         for r in rows
#     )
#     print(context)



# finally:
#     session.close()


# prompt = f"""You are a helpful agent.
#     Answer the question using ONLY the HDB transactions below.
#     If the answer isn't in the data, say you don't have enough information
#     Question: {question}
#     Transactions:
#     {context}"""

# answer = client.chat(
#     model="gemma4:e4b",
#     messages=[{"role": "user", "content": prompt}]
# )
# print(answer['message']['content'])

# from pydantic_ai import Agent, ModelSettings, RunContext
# from pydantic_ai.models.ollama import OllamaModel # Abstraction class representing how to talk to a provider's SDK
# from pydantic_ai.providers.ollama import OllamaProvider # In charge of authenticating and setting up the underlying http client
# from pydantic_ai.embeddings.openai import OpenAIEmbeddingModel

# # Gemma 4 recommended model settings
# gemma4_model_settings = ModelSettings(temperature=1.0, top_p=0.95, top_k=64)

# model = OllamaModel(
#     "gemma4:e4b", provider=OllamaProvider(
#         base_url=settings.ollama_base_url
#     )
# )

# agent = Agent(
#     model=model,
#     model_settings=gemma4_model_settings,
#     instructions=f"""You are a helpful agent.
#     "Answer the question using ONLY the HDB transactions below.
#     "If the answer isn't in the data, say you don't have enough information
#     Transactions:
#     {context}
    
#     Question: {question}"""
# )


# embedding_model = OpenAIEmbeddingModel(
#     "nomic-embed-text", provider=OllamaProvider(
#         base_url=settings.ollama_base_url
#     )
# )

# agent = Agent(
#     model,
#     model_settings=gemma4_model_settings,
#     # system_prompt=(
#     #     'You are an helpful pirate. Search, using Tavily, for the given query and use pirate language to answer.'
#     # ),
#     #instructions='Be concise, reply with one sentence',
#     #tools=[tavily_search_tool(api_key = settings.tavily_api_key, max_results=5, search_depth='fast')],
#     #capabilities=[Thinking(), WebSearch(local='duckduckgo')],
#     )


# # from pydantic_ai import Embedder
# # import tiktoken

# # embedder = Embedder(model=embedding_model)
# # async def main():
# #     # Embed a search query
# #     result = await embedder.embed_query('What is machine learning?')
# #     print(f'Embedding dimensions: {len(result.embeddings[0])}')
# #     #> Embedding dimensions: 1536
# #     # Embed multiple documents at once
# #     docs = [
# #         'Machine learning is a subset of AI.',
# #         'Deep learning uses neural networks.',
# #         'Python is a programming language.',
# #     ]
# #     result = await embedder.embed_documents(docs)
    
# #     encoding = tiktoken.get_encoding("cl100k_base") # Standard fast tokenizer
# #     # Calculate count manually
# #     token_count = len(encoding.encode(docs[0]))
# #     print(f"Token count (est): {token_count}")
# #     print(f'Embedded {len(result.embeddings)} documents')
# #     #> Embedded 3 documents


# # import asyncio

# # if __name__ == "__main__":
# #     asyncio.run(main())

# from rich import print as rprint

# result1 = agent.run_sync('Tell me a joke.')
# print(result1.output)
# #> Did you hear about the toothpaste scandal? They called it Colgate.
# result2 = agent.run_sync('Explain?', message_history=result1.new_messages())
# print(result2.output)
# #> This is an excellent joke invented by Samuel Colvin, it needs no explanation.
# rprint(result2.all_messages())



# agent.py

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.settings import ModelSettings
from ask_sg.core.config import settings
from ask_sg.agents.deps import AgentDeps
from ask_sg.integrations.embedding import embed_text
from ask_sg.repositories.agent_repo import get_embedding_rows


# Qwen3 Model Settings
qwen3_model_settings = ModelSettings(
    temperature=0.3,
    top_k=100,
    top_p=0.95
    )

# Qwen3 Model
qwen3_model = OllamaModel(
    model_name="qwen3:14b",
    provider=OllamaProvider(base_url=settings.ollama_base_url),
    settings=qwen3_model_settings
)

agent = Agent(
    model=qwen3_model,
    deps_type=AgentDeps,
    instructions="""You answer questions on HDB resale flats.
    Use the retrieve_from_database tool to fetch relevant transactions, and base your answer ONLY
    on the data it returns. If the tool returns nothing relevant, say you don't have enough 
    information to answer.
    If the question requires aggregation (averages, counts, totals) or exact filtering that
    the available tools cannot perform, say you cannot answer that type of question yet - do not
    estimate or guess.
    """
)


@agent.tool
def retrieve_from_database(
        ctx: RunContext[AgentDeps],
        query: str,
) -> str:
    """When to call this tool: When you need to perform semantic search against data in the
    database (e.g. What are the recent flats sold in the town area Bishan).
    When not to call this tool: When you need to perform a specific query against data in
    the database (e.g. Find all flats sold in Bishan or what is the average price of flats
    sold in Bishan)."""
    query_vector = embed_text(ctx.deps.client, query)
    rows = get_embedding_rows(
        ctx.deps.session,
        embedding_model=settings.ollama_embedding_model,
        query_vector=query_vector
    )
    return "\n".join(rows)




# agent_repo.py
from sqlalchemy import select
from ask_sg.models.orm import ResaleTransactions, ResaleTransactionsEmbeddings
from sqlalchemy.orm import Session
from collections.abc import Sequence

def get_embedding_rows(
        session: Session,
        embedding_model: str,
        query_vector: list[float],
        limit: int = 10
) -> Sequence[str]:
    distance = ResaleTransactionsEmbeddings.embedding.cosine_distance(query_vector).label("distance")
    stmt = (
        select(
            ResaleTransactions.embedding_text
        )
        .join(
            ResaleTransactionsEmbeddings,
            ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id
        )
        .where(
            ResaleTransactionsEmbeddings.embedding_model == embedding_model
        )
        .order_by(distance)
        .limit(limit)
    )
    return session.scalars(stmt).all()



# # Gemma4 Model Settings
# gemma4_model_settings = ModelSettings(
#     temperature=0.3,
#     top_k=64,
#     top_p=0.95
#     )

# # Gemma4 Model
# gemma4_model = OllamaModel(
#     model_name="gemma4:e4b",
#     provider=OllamaProvider(base_url=settings.ollama_base_url),
#     settings=gemma4_model_settings
#     )
