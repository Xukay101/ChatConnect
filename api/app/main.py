from fastapi import FastAPI

from app.config import settings
from app.routers.auth import router as auth_router

app = FastAPI()

@app.get(f'{settings.APP_PREFIX}/', tags=['root'])
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}

# Connect routers
app.include_router(auth_router, prefix=settings.APP_PREFIX)
