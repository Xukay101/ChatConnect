from datetime import datetime

from sqlmodel import Field, SQLModel, Column, String, Relationship

from app.utils import generate_id

class Message(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    sender_id: str = Field(foreign_key='user.id')
    room_id: str = Field(foreign_key='room.id')
    content: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    sender: 'User' = Relationship(back_populates='messages')
    room: 'Room' = Relationship(back_populates='messages')
