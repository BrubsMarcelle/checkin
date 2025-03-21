from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo para a tabela `users`
class User(BaseModel):
    id: str  # UUID
    username: str
    password_hash: str
    created_at: Optional[datetime] = None

# Modelo para a tabela `checkins`
class CheckIn(BaseModel):
    id: str  # UUID
    user_id: str  # UUID (Foreign Key para `users.id`)
    task_description: str
    checked_in_at: Optional[datetime] = None