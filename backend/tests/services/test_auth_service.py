import pytest
from fastapi import HTTPException
from pydantic.v1 import EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService


@pytest.fixture(autouse=True)
async def clean_database(async_session: AsyncSession):
    await async_session.execute(delete(User))
    await async_session.commit()
    yield


@pytest.mark.asyncio
async def test_auth_service_register_success(async_session):
    user_in = UserCreate(
        email=EmailStr("test@example.com"), password="testpassword"
    )
    result = await AuthService.register(user_in, async_session)

    assert result is not None
    assert result.user.email == user_in.email
    assert result.access_token is not None
    assert result.token_type == "bearer"
    assert result.expires_in is not None


@pytest.mark.asyncio
async def test_auth_service_register_user_exists(async_session):
    user_in = UserCreate(
        email=EmailStr("test@example.com"), password="testpassword"
    )
    await AuthService.register(user_in, async_session)

    with pytest.raises(HTTPException) as exc:
        await AuthService.register(user_in, async_session)

    assert exc.value.status_code == 400
    assert "User already exists" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_auth_service_login_success(async_session):
    user_in = UserCreate(
        email=EmailStr("test@example.com"), password="testpassword"
    )
    await AuthService.register(user_in, async_session)

    login_data = UserLogin(email=user_in.email, password=user_in.password)
    result = await AuthService.login(login_data, async_session)

    assert result is not None
    assert result.user.email == user_in.email
    assert result.access_token is not None
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_auth_service_login_invalid_credentials(async_session):
    login_data = UserLogin(email="test@example.com", password="wrongpassword")

    with pytest.raises(HTTPException) as exc:
        await AuthService.login(login_data, async_session)

    assert exc.value.status_code == 400
    assert "Invalid credentials" in str(exc.value.detail)
