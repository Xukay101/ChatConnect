import logging

from fastapi import FastAPI

from app.config import settings
from app.database import get_redis
from app.exc import RedisConnectionError

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event('startup')
async def startup_event():
    try:
        r = await get_redis()
        await r.ping()
        logger.info('Redis connection successful')
        await r.close()
    except Exception as e:
        logger.error(f'Error connecting to Redis: {str(e)}')
        raise RedisConnectionError('Failed to connect to Redis') from e    

@app.get(f'{settings.APP_PREFIX}/', tags=['root'])
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}

# Connect routers
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.chat import router as chat_router

routers = [
    auth_router,
    user_router,
    chat_router
]

for router in routers:
    app.include_router(router, prefix=settings.APP_PREFIX)
