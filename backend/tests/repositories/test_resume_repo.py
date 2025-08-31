import pytest

from app.repositories.resume_repo import (
    ResumeRepository,
    ResumeHistoryRepository,
)
from app.schemas.resume import ResumeCreate, ResumeUpdate


@pytest.mark.asyncio
async def test_resume_repository_create(async_session):
    repo = ResumeRepository(async_session)
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await repo.create(resume_in, user_id=1)

    assert resume.id is not None
    assert resume.title == "Test Resume"
    assert resume.content == "Sample content"
    assert resume.user_id == 1


@pytest.mark.asyncio
async def test_resume_repository_get_by_id(async_session):
    repo = ResumeRepository(async_session)
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await repo.create(resume_in, user_id=1)

    fetched_resume = await repo.get_by_id(resume.id)
    assert fetched_resume is not None
    assert fetched_resume.id == resume.id
    assert fetched_resume.title == resume.title

    assert await repo.get_by_id(999) is None


@pytest.mark.asyncio
async def test_resume_repository_update(async_session):
    repo = ResumeRepository(async_session)
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await repo.create(resume_in, user_id=1)

    update_data = ResumeUpdate(
        title="Updated Resume", content="Updated content"
    )
    updated_resume = await repo.update(resume.id, update_data)

    assert updated_resume is not None
    assert updated_resume.title == "Updated Resume"
    assert updated_resume.content == "Updated content"

    assert await repo.update(999, update_data) is None


@pytest.mark.asyncio
async def test_resume_repository_delete(async_session):
    repo = ResumeRepository(async_session)
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await repo.create(resume_in, user_id=1)

    deleted_resume = await repo.delete(resume.id)
    assert deleted_resume is not None
    assert deleted_resume.id == resume.id

    assert await repo.get_by_id(resume.id) is None

    assert await repo.delete(999) is None


@pytest.mark.asyncio
async def test_resume_history_repository_create_and_get_version(async_session):
    resume_repo = ResumeRepository(async_session)
    history_repo = ResumeHistoryRepository(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await resume_repo.create(resume_in, user_id=1)

    history_v1 = await history_repo.create(resume.id, "Version 1 content", 1)
    assert history_v1.id is not None
    assert history_v1.resume_id == resume.id
    assert history_v1.version == 1
    assert history_v1.content == "Version 1 content"

    max_version = await history_repo.get_max_version(resume.id)
    assert max_version == 1

    history_v2 = await history_repo.create(resume.id, "Version 2 content", 2)
    assert history_v2.version == 2

    max_version = await history_repo.get_max_version(resume.id)
    assert max_version == 2


@pytest.mark.asyncio
async def test_resume_history_repository_get_max_version_empty(async_session):
    history_repo = ResumeHistoryRepository(async_session)

    max_version = await history_repo.get_max_version(resume_id=999)
    assert max_version == 0
