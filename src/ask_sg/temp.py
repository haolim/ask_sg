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


