from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.services.user import get_user_by_id
from app.schemas.user import UserRead

router = APIRouter(prefix='/user', tags=['user'], responses={404: {'description': 'Not found'}})

@router.get('/{user_id}', status_code=200, response_model=UserRead)
async def get_user(user: User = Depends(get_user_by_id)):
    return user
