from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, WebSocket, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.config import settings
from app.models.user import User
from app.schemas.token import TokenPayload
from app.database import get_session, get_redis

# Token generation
def create_access_token(subject: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt

async def revoke_token(token: str, expires_in: int):
    r = await get_redis()
    await r.set(token, 'revoked', ex=expires_in)
    await r.aclose()

async def is_token_revoked(token: str) -> bool:
    r = await get_redis()
    token_status = await r.get(token)
    await r.aclose()
    if token_status:
        return token_status.decode('utf-8')  == 'revoked'
    return False

class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    # Check if token in blacklist
    token_revoked = await is_token_revoked(token)
    if token_revoked:
        raise HTTPException(status_code=401, detail='Token has been revoked')

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail='Access Token expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # Get user
        query = select(User).where(User.id == token_data.sub)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User not found',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        
        return user


    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

async def get_token_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail='Could not validate token')
