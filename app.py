import os
import uvicorn
from fastapi import FastAPI
from time import time
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.config.config import APP_HOST, APP_PORT, DEBUG
from src.middlewares.logging import log_middleware
from src.routes.todo_route import router as todo_router

# load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register middlewares
app.middleware("http")(log_middleware)

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API"}

# register routes
app.include_router(todo_router, tags=["Todos"])
                
if __name__ == "__main__":
    uvicorn.run("app:app", host=APP_HOST, port=APP_PORT, reload=DEBUG)