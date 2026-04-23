from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = [] #toddo items

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: str):
    items.append(item)
    print(items)
    return {"message": f"Item '{item}' created successfully."}

@app.get("/items/{items_id}")
async def read_item(items_id: int):
    item = items[items_id]
    return {"item_id": items_id, "item": item}