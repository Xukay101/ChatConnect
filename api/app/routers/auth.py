from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, or_
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserCreate
from app.schemas.token import Token
from app.services.auth import create_access_token
from app.services.security import get_hashed_password, verify_password

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {'description': 'Not found'}})

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

@router.get('/login', status_code=200, response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    # Get user from database
    query = select(User).where(User.username == form_data.username)
    result = await session.execute(query)
    user = result.scalars().first()

    # Check if username is valid
    if not user: 
        raise HTTPException(401, 'Incorrect username or password')

    # Check if password is valid
    if not verify_password(form_data.password, user.password):
        raise HTTPException(401, 'Incorrect username or password')

    # Create JWT Token
    access_token = create_access_token(user.id) 
    
    return {'access_token': access_token, 'token_type': 'bearer'}
