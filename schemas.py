from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    is_completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(BaseModel):
    id: int
    title: str
    is_completed: bool

    class Config:
        orm_mode = True

class BulkTaskCreate(BaseModel):
    tasks: List[TaskCreate]

class BulkTaskDelete(BaseModel):
    tasks: List[int]
