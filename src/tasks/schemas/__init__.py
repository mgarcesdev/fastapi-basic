from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskOut(BaseModel):
    id: str  # Usamos str para que funcione tanto con Mongo como con SQL
    description: str
    is_completed: bool
    created_at: datetime


class TaskCreate(BaseModel):
    description: str


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None
