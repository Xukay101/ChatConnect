from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, or_
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserCreate
from app.schemas.token import Token, TokenPayload
from app.services.security import get_hashed_password, verify_password
from app.services.auth import (
    create_access_token,
    get_current_user, 
    get_token_payload, 
    oauth2_scheme,
    revoke_token
)

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {'description': 'Not found'}})

@router.post('/register', status_code=201, response_model=UserRead)
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

@router.post('/login', status_code=200, response_model=Token)
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

@router.get('/verify', status_code=200)
async def verify_token(current_user: int = Depends(get_current_user)):
    return {'status': 'Token is valid', 'user_id': current_user.id}

@router.post('/logout', status_code=200)
async def logout(payload: TokenPayload = Depends(get_token_payload), token: str = Depends(oauth2_scheme)):
    now = datetime.now(timezone.utc)
    expires_in = payload.exp - int(now.timestamp())

    if expires_in <= 0:
        raise HTTPException(status_code=400, detail='Token is already expired')

    await revoke_token(token, expires_in)
    return {'detail': 'Token has been revoked'}
