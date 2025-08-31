import pytest
from pydantic import ValidationError
from app.schemas.resume import (
    ResumeCreate, ResumeImprove, ResumeUpdate,
    ResumeResponse, ResumeHistoryResponse,
)


@pytest.mark.asyncio
async def test_resume_create_schema_valid():
    """Тестирование валидации корректных данных для ResumeCreate."""
    data = {
        "title": "Software Engineer Resume",
        "content": "Experienced developer with 5 years of experience..."
    }
    resume = ResumeCreate(**data)

    assert resume.title == "Software Engineer Resume"
    assert resume.content == "Experienced developer with 5 years of experience..."


@pytest.mark.asyncio
async def test_resume_create_schema_missing_fields():
    """Тестирование валидации ResumeCreate с отсутствующими обязательными полями."""
    data = {"title": "Software Engineer Resume"}

    with pytest.raises(ValidationError) as exc:
        ResumeCreate(**data)

    assert "Field required" in str(exc.value)


@pytest.mark.asyncio
async def test_resume_improve_schema_valid():
    """Тестирование валидации корректных данных для ResumeImprove."""
    data = {"content": "Improved resume content"}
    resume = ResumeImprove(**data)

    assert resume.content == "Improved resume content"


@pytest.mark.asyncio
async def test_resume_improve_schema_missing_fields():
    """Тестирование валидации ResumeImprove с отсутствующими обязательными полями."""
    data = {}

    with pytest.raises(ValidationError) as exc:
        ResumeImprove(**data)

    assert "Field required" in str(exc.value)


@pytest.mark.asyncio
async def test_resume_update_schema_valid():
    """Тестирование валидации корректных данных для ResumeUpdate."""
    data = {
        "title": "Updated Resume Title",
        "content": "Updated resume content"
    }
    resume = ResumeUpdate(**data)

    assert resume.title == "Updated Resume Title"
    assert resume.content == "Updated resume content"


@pytest.mark.asyncio
async def test_resume_update_schema_none_fields():
    """Тестирование валидации ResumeUpdate с None полями."""
    data = {"title": None, "content": "Partial update content"}
    resume = ResumeUpdate(**data)

    assert resume.title is None
    assert resume.content == "Partial update content"


@pytest.mark.asyncio
async def test_resume_response_schema_valid():
    """Тестирование валидации корректных данных для ResumeResponse."""
    data = {
        "id": 1,
        "title": "Test Resume",
        "content": "Test content",
        "user_id": 100
    }
    resume = ResumeResponse(**data)

    assert resume.id == 1
    assert resume.title == "Test Resume"
    assert resume.content == "Test content"
    assert resume.user_id == 100


@pytest.mark.asyncio
async def test_resume_response_schema_missing_fields():
    """Тестирование валидации ResumeResponse с отсутствующими обязательными полями."""
    data = {
        "id": 1,
        "title": "Test Resume",
        "user_id": 100
    }

    with pytest.raises(ValidationError) as exc:
        ResumeResponse(**data)

    assert "Field required" in str(exc.value)


@pytest.mark.asyncio
async def test_resume_history_response_schema_valid():
    """Тестирование валидации корректных данных для ResumeHistoryResponse."""
    data = {
        "id": 1,
        "resume_id": 10,
        "version": 1,
        "content": "Version 1 content",
        "created_at": "2023-01-01T12:00:00"
    }
    resume = ResumeHistoryResponse(**data)

    assert resume.id == 1
    assert resume.resume_id == 10
    assert resume.version == 1
    assert resume.content == "Version 1 content"
    assert resume.created_at == "2023-01-01T12:00:00"


@pytest.mark.asyncio
async def test_resume_history_response_schema_missing_fields():
    """Тестирование валидации ResumeHistoryResponse с отсутствующими обязательными полями."""
    data = {
        "id": 1,
        "resume_id": 10,
        "version": 1,
        "created_at": "2023-01-01T12:00:00"
    }

    with pytest.raises(ValidationError) as exc:
        ResumeHistoryResponse(**data)

    assert "Field required" in str(exc.value)


@pytest.mark.asyncio
async def test_resume_history_response_schema_invalid_types():
    """Тестирование валидации ResumeHistoryResponse с некорректными типами данных."""
    data = {
        "id": "1",  # Should be int, not str
        "resume_id": 10,
        "version": 1,
        "content": "Version 1 content",
        "created_at": "2023-01-01T12:00:00"
    }

    with pytest.raises(ValidationError) as exc:
        ResumeHistoryResponse(**data)

    assert "Input should be a valid integer" in str(exc.value)
