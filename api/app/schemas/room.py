from datetime import datetime

from pydantic import BaseModel

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: str
    code: str
    created_at: datetime
