from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional

from src.schemas.todo_schema import Todo, ReturnTodo

router = APIRouter()

todos = []

async def send_email(todo: Todo):
    print(f"Email notification for Todo {todo.id} sent!")

@router.post("/todos", response_model=ReturnTodo)
async def add_todos(todo: Todo, background_task: BackgroundTasks):
    todo.id = len(todos) + 1
    todos.append(todo)
    background_task.add_task(send_email, todo)
    return todo 

@router.get("/todos")
async def read_todos(completed: Optional[bool] = None):
    if completed is None:
        return todos
    else:
        return [todo for todo in todos if todo.is_completed == completed]

@router.get("/todos/{id}")
async def read_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/todos/{id}")
async def update_todo(id: int, new_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == id:
            todos[index] = new_todo
            todos[index].id = id
            return
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/todos/{id}")
async def delete_todo(id: int):
    for index, todo in enumerate(todos):
        if todo.id == id:
            del todos[index]
            return 
    raise HTTPException(status_code=404, detail="Todo not found")