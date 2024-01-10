from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, or_
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.utils import get_hashed_password
from app.models.user import User
from app.schemas.user import UserRead, UserCreate

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {'description': 'Not found'}})

@router.get('/')
async def root():
    return {'message': 'Auth Router Root Endpoint'}

@router.get('/register', status_code=201, response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user or email already exist
    query = select(User).where(or_(User.username == user.username, User.email == user.email))
    result = await session.execute(query)
    user_found = result.scalars().first()
    if user_found:
        raise HTTPException(409, 'User already exists')

    # Hashing password
    user.password = get_hashed_password(user.password)

    # Create a new user instance
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
