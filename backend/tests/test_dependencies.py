import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import swagger_auth, get_current_user
from app.schemas.user import UserResponse


def test_swagger_auth_valid_credentials():
    """Тестирование swagger_auth с корректными учетными данными."""
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="testtoken123"
    )
    result = swagger_auth(credentials)
    assert result == credentials
    assert result.credentials == "testtoken123"
    assert result.scheme == "Bearer"


def test_swagger_auth_no_credentials():
    """Тестирование swagger_auth без учетных данных."""
    result = swagger_auth(None)
    assert result is None


@pytest.mark.asyncio
async def test_get_current_user_valid_token_and_user():
    """Тестирование get_current_user с корректным токеном и существующим пользователем."""
    decode_jwt_mock = MagicMock(return_value={"sub": "test@example.com"})

    user = MagicMock()
    user.id = 1
    user.email = "test@example.com"
    user_repo_mock = AsyncMock(return_value=user)

    db = AsyncMock(spec=AsyncSession)

    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.dependencies.decode_jwt", decode_jwt_mock)
        m.setattr(
            "app.dependencies.UserRepository", MagicMock(
                return_value=MagicMock(get_by_email=user_repo_mock)
            )
        )

        result = await get_current_user(token="testtoken123", db=db)

    assert isinstance(result, UserResponse)
    assert result.id == 1
    assert result.email == "test@example.com"
    decode_jwt_mock.assert_called_once_with("testtoken123")
    user_repo_mock.assert_awaited_once_with(email="test@example.com")


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Тестирование get_current_user с некорректным токеном."""
    decode_jwt_mock = MagicMock(
        side_effect=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    )

    db = AsyncMock(spec=AsyncSession)

    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.dependencies.decode_jwt", decode_jwt_mock)

        with pytest.raises(HTTPException) as exc:
            await get_current_user(token="invalidtoken", db=db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
    decode_jwt_mock.assert_called_once_with("invalidtoken")


@pytest.mark.asyncio
async def test_get_current_user_no_email_in_token():
    """Тестирование get_current_user с токеном без поля sub."""
    decode_jwt_mock = MagicMock(return_value={})

    db = AsyncMock(spec=AsyncSession)

    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.dependencies.decode_jwt", decode_jwt_mock)

        with pytest.raises(HTTPException) as exc:
            await get_current_user(token="testtoken123", db=db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
    decode_jwt_mock.assert_called_once_with("testtoken123")


@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    """Тестирование get_current_user с корректным токеном, но без пользователя в базе."""
    decode_jwt_mock = MagicMock(return_value={"sub": "test@example.com"})

    user_repo_mock = AsyncMock(return_value=None)

    db = AsyncMock(spec=AsyncSession)

    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.dependencies.decode_jwt", decode_jwt_mock)
        m.setattr(
            "app.dependencies.UserRepository", MagicMock(
                return_value=MagicMock(get_by_email=user_repo_mock)
            )
        )

        with pytest.raises(HTTPException) as exc:
            await get_current_user(token="testtoken123", db=db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
    decode_jwt_mock.assert_called_once_with("testtoken123")
    user_repo_mock.assert_awaited_once_with(email="test@example.com")
