# backend/app/main.py
from fastapi import FastAPI
from app.routers import boards, lists, cards, users


app = FastAPI()
app.include_router(boards.router)
app.include_router(lists.router)
app.include_router(cards.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Hello World!"}
