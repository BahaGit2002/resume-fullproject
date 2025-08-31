import pytest
from fastapi import HTTPException
from app.repositories.resume_repo import ResumeHistoryRepository
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeImprove
from app.services.resume_service import ResumeService
from app.models.user import User


async def create_user(async_session, email="test@example.com") -> User:
    user = User(email=email, hashed_password="test")
    async_session.add(user)
    await async_session.commit()
    return user


@pytest.mark.asyncio
async def test_create_resume(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    assert resume.id is not None
    assert resume.title == "Test Resume"
    assert resume.content == "Sample content"
    assert resume.user_id == user.id


@pytest.mark.asyncio
async def test_get_resumes_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    await ResumeService.create_resume(resume_in, async_session, user.id)

    resumes = await ResumeService.get_resumes(user.email, async_session)
    assert len(resumes) == 1
    assert resumes[0].title == "Test Resume"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resumes(
            "nonexistent@example.com", async_session
        )
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


@pytest.mark.asyncio
async def test_get_resume_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    fetched = await ResumeService.get_resume(resume.id, async_session)
    assert fetched.id == resume.id
    assert fetched.title == resume.title

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resume(999, async_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Resume not found"


@pytest.mark.asyncio
async def test_update_resume_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    update_data = ResumeUpdate(
        title="Updated Resume", content="Updated content"
    )
    updated = await ResumeService.update_resume(
        resume.id, update_data, async_session
    )

    assert updated.title == "Updated Resume"
    assert updated.content == "Updated content"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.update_resume(999, update_data, async_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Resume not found"


@pytest.mark.asyncio
async def test_delete_resume_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    await ResumeService.delete_resume(resume.id, async_session)
    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resume(resume.id, async_session)
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc:
        await ResumeService.delete_resume(999, async_session)
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail.lower()


@pytest.mark.asyncio
async def test_improve_resume_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    improve_data = ResumeImprove(content="Improved content")
    improved = await ResumeService.improve_resume(
        resume.id, improve_data, async_session
    )

    assert improved.content == "Improved content [Improved]"

    history_repo = ResumeHistoryRepository(async_session)
    max_version = await history_repo.get_max_version(resume.id)
    assert max_version == 1

    improve_data2 = ResumeImprove(content="Second improvement")
    await ResumeService.improve_resume(resume.id, improve_data2, async_session)
    max_version = await history_repo.get_max_version(resume.id)
    assert max_version == 2

    with pytest.raises(HTTPException) as exc:
        await ResumeService.improve_resume(999, improve_data, async_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Resume not found"
