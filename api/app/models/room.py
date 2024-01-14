from typing import List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship, Column

from app.utils import generate_id, generate_code

class Room(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str
    code: str = Field(default_factory=generate_code, unique=True, nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    messages: List['Message'] = Relationship(back_populates='room')
