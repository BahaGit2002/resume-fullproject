from datetime import datetime, timezone, timedelta

import jwt
import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import (
    hash_password, verify_password, create_jwt,
    decode_jwt,
)


@pytest.mark.asyncio
async def test_hash_password():
    password = "testpassword"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


@pytest.mark.asyncio
async def test_verify_password_correct():
    password = "testpassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


@pytest.mark.asyncio
async def test_verify_password_incorrect():
    password = "testpassword"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False


@pytest.mark.asyncio
async def test_create_jwt():
    data = {"sub": "1"}
    token = create_jwt(data)

    assert token is not None
    decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded["sub"] == "1"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_decode_jwt_valid():
    data = {"sub": "1"}
    token = create_jwt(data)
    decoded = decode_jwt(token)

    assert decoded["sub"] == "1"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_decode_jwt_expired():
    data = {"sub": "1"}
    expires = datetime.now(timezone.utc) - timedelta(
        minutes=1
    )
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(HTTPException) as exc:
        decode_jwt(token)

    assert exc.value.status_code == 401
    assert "Token expired" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_decode_jwt_invalid():
    invalid_token = "invalid.token.string"

    with pytest.raises(HTTPException) as exc:
        decode_jwt(invalid_token)

    assert exc.value.status_code == 401
    assert "Invalid token" in str(exc.value.detail)
