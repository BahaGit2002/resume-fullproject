import pytest
from pydantic.v1 import EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_user_repository_create(async_session):
    user_in = UserCreate(
        email=EmailStr("test@example.com"), password="testpassword"
    )
    user_repo = UserRepository(async_session)

    user = await user_repo.create(user_in)

    assert user is not None
    assert user.email == user_in.email
    assert user.hashed_password is not None
    assert verify_password(user_in.password, user.hashed_password)


@pytest.mark.asyncio
async def test_user_repository_get_by_email(async_session):
    user_in = UserCreate(
        email=EmailStr("test@example.com"), password="testpassword"
    )
    user_repo = UserRepository(async_session)

    await user_repo.create(user_in)

    user = await user_repo.get_by_email(str(user_in.email))
    assert user is not None
    assert user.email == user_in.email

    assert user is not None
    assert user.email == user_in.email


@pytest.mark.asyncio
async def test_user_repository_get_by_email_not_found(async_session):
    user_repo = UserRepository(async_session)
    user = await user_repo.get_by_email("nonexistent@example.com")

    assert user is None
