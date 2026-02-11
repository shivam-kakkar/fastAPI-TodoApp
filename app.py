from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from time import time
from fastapi.middleware.cors import CORSMiddleware

class BaseTodo(BaseModel):
    task: str

class Todo(BaseTodo):
    id: Optional[int] = None
    is_completed: bool = False

class ReturnTodo(BaseTodo):
    pass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

todos = []

@app.middleware("http")
async def log_middleware(request, call_next):
    print("Before route")
    start_time = time()
    response = await call_next(request)
    end_time = time()
    process_time = end_time - start_time
    print(f"Request {request.url} processed in {process_time} seconds")
    return response

async def send_email(todo: Todo):
    print(f"Email notification for Todo {todo.id} sent!")

@app.post("/todos", response_model=ReturnTodo)
async def add_todos(todo: Todo, background_task: BackgroundTasks):
    todo.id = len(todos) + 1
    todos.append(todo)
    background_task.add_task(send_email, todo)
    return todo 

@app.get("/todos")
async def read_todos(completed: Optional[bool] = None):
    if completed is None:
        return todos
    else:
        return [todo for todo in todos if todo.is_completed == completed]

@app.get("/todos/{id}")
async def read_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{id}")
async def update_todo(id: int, new_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == id:
            todos[index] = new_todo
            todos[index].id = id
            return
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    for index, todo in enumerate(todos):
        if todo.id == id:
            del todos[index]
            return 
    raise HTTPException(status_code=404, detail="Todo not found")
    