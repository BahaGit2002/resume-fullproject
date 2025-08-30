from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPAuthorizationCredentials, HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_jwt
from app.database import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer(auto_error=False)


def swagger_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    return credentials


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except HTTPException:
        raise

    user = await UserRepository(db).get_by_email(email=email)
    if user is None:
        raise credentials_exception
    return UserResponse.model_validate(user)
