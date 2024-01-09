from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_db

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {'description': 'Not found'}})

@router.get('/')
async def root():
    return {'message': 'Auth Router Root Endpoint'}

@router.get('/test')
async def test(db: AsyncSession = Depends(get_db)):
    print(db)
    return {'message': 'Test endpoint'}
