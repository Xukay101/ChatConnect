import redis.asyncio as redis
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create an async database engine
async_engine = create_async_engine(
    settings.DATABASE_URI,
    echo=False,
    future=True
)

# Create a local session class using the async engine
local_session = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Define an async function to get the mysql database session
async def get_session() -> AsyncSession:
    async_session = local_session
    
    async with async_session() as db:
        yield db
        await db.commit()

# Define an async function to get the redis database session
async def get_redis():
    return redis.from_url(settings.REDIS_URI)
