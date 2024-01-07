from fastapi import FastAPI

from app.config import settings

app = FastAPI()

@app.get('/', tags=['root'])
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}
