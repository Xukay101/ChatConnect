from datetime import datetime

from sqlmodel import Field, SQLModel, Column, String
from pydantic import EmailStr

from app.utils import generate_id

class User(SQLModel, table=True): # Refactorizar para que genere un id con nanoid
    # id: str = Field(primary_key=True)
    id: str = Field(default_factory=generate_id, primary_key=True)
    first_name: str
    last_name: str
    username: str = Field(sa_column=Column(String(50), index=True, unique=True))
    email: EmailStr = Field(sa_column=Column(String(999), index=True, unique=True))
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
