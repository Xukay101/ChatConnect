from fastapi import ( 
    APIRouter, 
    Depends, 
    HTTPException, 
    WebSocket, 
    Request, 
    WebSocketDisconnect,
)
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.message import Message
from app.models.user import User
from app.models.room import Room
from app.schemas.message import MessageRead, MessageCreate
from app.schemas.room import RoomRead, RoomCreate
from app.services.auth import get_current_user
from app.services.chat import get_room_websocket, save_message

router = APIRouter(prefix='/chat', tags=['chat'], responses={404: {'description': 'Not found'}})

@router.websocket('/ws/{room_id}')
async def socket(
    websocket: WebSocket,
    room_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Walidate if room exist
    query = select(Room).where(Room.id == room_id).options(selectinload(Room.messages))
    result = await session.execute(query)
    room = result.scalars().first()
    if not room:
        raise WebSocketDisconnect()

    get_room_websocket(room_id)[current_user.id] = websocket

    try:
        await websocket.accept()
        await websocket.send_text(f'Welcome to the room {room.name}')

        messages = room.messages
        for message in messages:
            await websocket.send_text(f'[{message.created_at}] {message.sender.username}: {message.content}')

        while True:
            data = await websocket.receive_text()
            message_data = MessageCreate(content=data, sender_id=current_user.id, room_id=room_id)

            # Save message in database
            message = await save_message(message_data, session)

            # Send message to all users
            for user_id, ws in get_room_websocket(room_id).items():
                if user_id != current_user.id:
                    await ws.send_text(f'[{message.created_at}] {message.sender.username}: {message.content}')

    except WebSocketDisconnect as e:
        # Handle disconnect
        del get_room_websocket(room_id)[current_user.id]
        await websocket.close(reason=e)

@router.post('/room/', status_code=201, response_model=RoomRead)
async def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_room = Room(**room_data.model_dump())

    session.add(new_room)
    await session.commit()
    await session.refresh(new_room)

    return new_room
