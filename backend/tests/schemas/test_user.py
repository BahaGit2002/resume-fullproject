import pytest
from pydantic import ValidationError
from app.schemas.user import UserBase, UserCreate, UserLogin, UserResponse


@pytest.mark.asyncio
async def test_user_base_schema_valid():
    """Тестирование валидации корректных данных для UserBase."""
    data = {"email": "test@example.com"}
    user_base = UserBase(**data)

    assert user_base.email == "test@example.com"
    assert isinstance(user_base.email, str)


@pytest.mark.asyncio
async def test_user_base_schema_invalid_email():
    """Тестирование валидации некорректного email в UserBase."""
    data = {"email": "invalid-email"}

    with pytest.raises(ValidationError) as exc:
        UserBase(**data)

    assert "value is not a valid email address" in str(exc.value)


@pytest.mark.asyncio
async def test_user_create_schema_valid():
    """Тестирование валидации корректных данных для UserCreate."""
    data = {"email": "test@example.com", "password": "testpassword"}
    user_create = UserCreate(**data)

    assert user_create.email == "test@example.com"
    assert user_create.password == "testpassword"


@pytest.mark.asyncio
async def test_user_create_schema_missing_password():
    """Тестирование валидации UserCreate без пароля."""
    data = {"email": "test@example.com"}

    with pytest.raises(ValidationError) as exc:
        UserCreate(**data)

    assert "Field required" in str(exc.value)  # Проверяем часть сообщения


@pytest.mark.asyncio
async def test_user_login_schema_valid():
    """Тестирование валидации корректных данных для UserLogin."""
    data = {"email": "test@example.com", "password": "testpassword"}
    user_login = UserLogin(**data)

    assert user_login.email == "test@example.com"
    assert user_login.password == "testpassword"


@pytest.mark.asyncio
async def test_user_login_schema_invalid_email():
    """Тестирование валидации UserLogin с некорректным email."""
    data = {"email": "invalid-email", "password": "testpassword"}

    with pytest.raises(ValidationError) as exc:
        UserLogin(**data)

    assert "value is not a valid email address" in str(exc.value)


@pytest.mark.asyncio
async def test_user_response_schema_valid():
    """Тестирование валидации корректных данных для UserResponse."""
    data = {"id": 1, "email": "test@example.com"}
    user_response = UserResponse(**data)

    assert user_response.id == 1
    assert user_response.email == "test@example.com"


@pytest.mark.asyncio
async def test_user_response_schema_missing_id():
    """Тестирование валидации UserResponse без id."""
    data = {"email": "test@example.com"}

    with pytest.raises(ValidationError) as exc:
        UserResponse(**data)

    assert "Field required" in str(exc.value)
