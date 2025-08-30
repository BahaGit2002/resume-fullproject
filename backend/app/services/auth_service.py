from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_jwt, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.auth import TokenWithUser
from app.schemas.user import UserCreate, UserResponse, UserLogin


class AuthService:
    @staticmethod
    async def register(user_in: UserCreate, db: AsyncSession) -> TokenWithUser:
        user_repo = UserRepository(db)
        if await user_repo.get_by_email(str(user_in.email)):
            raise HTTPException(status_code=400, detail="User already exists")

        user = await user_repo.create(user_in)
        token = create_jwt({"sub": str(user.email)})
        return TokenWithUser(
            user=UserResponse.model_validate(user),
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES
        )

    @staticmethod
    async def login(user_in: UserLogin, db: AsyncSession) -> TokenWithUser:
        user_repo = UserRepository(db)
        user = await user_repo.get_by_email(str(user_in.email))
        if not user or not verify_password(user_in.password, str(user.hashed_password)):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = create_jwt({"sub": str(user.email)})
        return TokenWithUser(
            user=UserResponse.model_validate(user),
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES
        )
