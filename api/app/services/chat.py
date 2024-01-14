from typing import Dict, Optional

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message 
from app.schemas.message import MessageCreate

active_websockets: Dict[str, Dict[str, WebSocket]] = {}

async def save_message(message_data: MessageCreate, session: AsyncSession):
    new_message = Message(**message_data.model_dump())
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)

    return new_message

def get_room_websocket(room_id: str) -> Dict[str, WebSocket]:
    return active_websockets.setdefault(room_id, {})
