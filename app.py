import uvicorn
from fastapi import FastAPI
from time import time
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares.logging import log_middleware
from src.routes.todo_route import router as todo_router

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
    uvicorn.run("app:app", host="127.0.0.1", port=5566, reload=True)