from pydantic import BaseModel
from typing import Optional

class BaseTodo(BaseModel):
    task: str

class Todo(BaseTodo):
    id: Optional[int] = None
    is_completed: bool = False

class ReturnTodo(BaseTodo):
    pass