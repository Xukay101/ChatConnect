from datetime import datetime

from pydantic import BaseModel

class MessageBase(BaseModel):
    sender_id: str
    room_id: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: str
    created_at: datetime

class MessageUpdate(BaseModel):
    content: str | None = None
