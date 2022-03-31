from typing import Optional
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()
# ------------


# 리퀘스트 바디까지 함
# ------------
# BaseModel을 통해 미리 body형식을 지정할 수 있음
class Book(BaseModel):
    name: str
    description: Optional[str] = None  # 3.10버전 -> description: str | None = None
    price: float
    tax: Optional[float] = None


@app.post("/Books/")
async def create_book(book: Book): # Body(...) 를 사용하면 자유형식으로 파라미터를 받을 수 있음. fastapi import Body 필요
    print(type(book)) # >>> <class 'main.Book'>
    print(book.name) # >>> string // dict는 아님
    return book #들어온 body를 객체형태로 받아서 바로 사용가능



# ------------
# 파라미터에 기본값을 지정하지 않으면 필수로 받는다.
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# ------------
# Optional은 FastAPI(FastAPI는 str 부분만 사용합니다)가 사용하는게 아니지만, Optional[str]은 편집기에게 코드에서 오류를 찾아낼 수 있게 도와줍니다.
# typing 모듈의 Optional은 None이 허용되는 함수의 매개 변수에 대한 타입을 명시할 때 유용합니다. 
# Optional[int]는 Union[int, None]과 동일한 효력을 갖습니다.
# num: Union[int, float] -> 여러 타입을 지정할 수 있다.
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
): # 인풋의 bool 여부를 체크해줌
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# ------------
# 쿼리 파라미터는 경로에 적지 않고 함수 파라미터에 기재
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): # 형태 > (받는 변수명: 타입 = 기본값)
    return fake_items_db[skip : skip + limit] # >>> [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]





# ------------
# path를 패스파라미터로 받는 경우
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path} # >>> {"file_path":"home/johndoe/myfile.txt"}


# ------------
# 오른쪽 값이 받아들이려는 값이다.
# 패스파라미터로 들어오는 것은 str이다.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name, model_name.value) # ModelName.lenet, lenet
    
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
# ------------



@app.get("/")
async def root():
    return {"message": "Hello World"}
            
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
