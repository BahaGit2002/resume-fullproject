from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import TokenWithUser
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenWithUser, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(user_in, db)


@router.post("/login", response_model=TokenWithUser, status_code=200)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(user_in, db)
