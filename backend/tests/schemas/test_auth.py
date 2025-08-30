import pytest
from pydantic import ValidationError
from app.schemas.auth import Token, TokenWithUser


@pytest.mark.asyncio
async def test_token_schema_valid():
    """Тестирование валидации корректных данных для Token."""
    data = {
        "access_token": "testtoken123",
        "token_type": "bearer",
        "expires_in": 30
    }
    token = Token(**data)

    assert token.access_token == "testtoken123"
    assert token.token_type == "bearer"
    assert token.expires_in == 30


@pytest.mark.asyncio
async def test_token_schema_missing_fields():
    """Тестирование валидации Token с отсутствующими обязательными полями."""
    data = {"access_token": "testtoken123"}

    with pytest.raises(ValidationError) as exc:
        Token(**data)

    assert "Field required" in str(exc.value)


@pytest.mark.asyncio
async def test_token_schema_none_expires_in():
    """Тестирование валидации Token с expires_in = None."""
    data = {
        "access_token": "testtoken123",
        "token_type": "bearer",
        "expires_in": None
    }
    token = Token(**data)

    assert token.access_token == "testtoken123"
    assert token.token_type == "bearer"
    assert token.expires_in is None


@pytest.mark.asyncio
async def test_token_with_user_schema_valid():
    """Тестирование валидации корректных данных для TokenWithUser."""
    data = {
        "access_token": "testtoken123",
        "token_type": "bearer",
        "expires_in": 30,
        "user": {"id": 1, "email": "test@example.com"}
    }
    token_with_user = TokenWithUser(**data)

    assert token_with_user.access_token == "testtoken123"
    assert token_with_user.token_type == "bearer"
    assert token_with_user.expires_in == 30
    assert token_with_user.user.id == 1
    assert token_with_user.user.email == "test@example.com"


@pytest.mark.asyncio
async def test_token_with_user_schema_invalid_user():
    """Тестирование валидации TokenWithUser с некорректным user."""
    data = {
        "access_token": "testtoken123",
        "token_type": "bearer",
        "expires_in": 30,
        "user": {"id": 1}
    }

    with pytest.raises(ValidationError) as exc:
        TokenWithUser(**data)

    assert "Field required" in str(exc.value)
