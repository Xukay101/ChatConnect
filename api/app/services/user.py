from fastapi import HTTPException, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.database import get_session

async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(404, detail='User not found')
    return user

