from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    last_name: str
    first_name: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    last_name: str | None = None
    first_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
