from pydantic import BaseModel

class Task(BaseModel):
    task: str
    completed: bool = False

class User(BaseModel):
    username: str
    password: str
    