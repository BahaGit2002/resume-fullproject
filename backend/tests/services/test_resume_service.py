import pytest
from fastapi import HTTPException
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeImprove
from app.services.resume_service import ResumeService


async def create_user(async_session, email="test@example.com") -> User:
    user = User(email=email, hashed_password="test")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
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
    await async_session.refresh(user)

    resumes = await ResumeService.get_resumes(user.email, async_session)
    assert len(resumes) == 1
    assert resumes[0].title == "Test Resume"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resumes(
            "nonexistent@example.com", async_session
        )
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_get_resume_success_and_errors(async_session):
    user = await create_user(async_session)
    other_user = await create_user(async_session, email="other@example.com")

    resume = await ResumeService.create_resume(
        ResumeCreate(title="Test", content="Content"), async_session, user.id
    )

    fetched = await ResumeService.get_resume(resume.id, user, async_session)
    assert fetched.id == resume.id

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resume(999, user, async_session)
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resume(resume.id, other_user, async_session)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_update_resume_success_and_errors(async_session):
    user = await create_user(async_session)
    other_user = await create_user(async_session, email="other@example.com")
    resume = await ResumeService.create_resume(
        ResumeCreate(title="Test", content="Content"), async_session, user.id
    )

    update_data = ResumeUpdate(title="Updated", content="Updated content")
    updated = await ResumeService.update_resume(
        resume.id, update_data, async_session, user
    )
    assert updated.title == "Updated"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.update_resume(
            999, update_data, async_session, user
        )
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc:
        await ResumeService.update_resume(
            resume.id, update_data, async_session, other_user
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_delete_resume_success_and_errors(async_session):
    user = await create_user(async_session)
    other_user = await create_user(async_session, email="other@example.com")
    resume = await ResumeService.create_resume(
        ResumeCreate(title="Test", content="Content"), async_session, user.id
    )

    await ResumeService.delete_resume(resume.id, async_session, user)
    with pytest.raises(HTTPException):
        await ResumeService.get_resume(resume.id, user, async_session)

    resume2 = await ResumeService.create_resume(
        ResumeCreate(title="Other", content="Other"), async_session, user.id
    )
    with pytest.raises(HTTPException) as exc:
        await ResumeService.delete_resume(
            resume2.id, async_session, other_user
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_improve_resume_success_and_errors(async_session):
    user = await create_user(async_session)
    other_user = await create_user(async_session, email="other@example.com")

    resume = await ResumeService.create_resume(
        ResumeCreate(title="Test", content="Content"), async_session, user.id
    )

    improve_data = ResumeImprove(content="Improved")
    improved = await ResumeService.improve_resume(
        resume.id, improve_data, async_session, user
    )
    assert improved.content == "Improved [Improved]"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.improve_resume(
            999, improve_data, async_session, user
        )
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc:
        await ResumeService.improve_resume(
            resume.id, improve_data, async_session, other_user
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_get_resume_history_success_and_not_found(async_session):
    user = await create_user(async_session)

    resume = await ResumeService.create_resume(
        ResumeCreate(title="Test Resume", content="Sample content"),
        async_session, user.id
    )

    histories = await ResumeService.get_resume_history(
        resume.id, user, async_session
    )
    assert histories == []

    improve_data = ResumeImprove(content="Improved content")
    await ResumeService.improve_resume(
        resume.id, improve_data, async_session, user
    )

    histories = await ResumeService.get_resume_history(
        resume.id, user, async_session
    )
    assert len(histories) == 1
    assert histories[0].content == "Improved content [Improved]"

    with pytest.raises(HTTPException) as exc:
        await ResumeService.get_resume_history(999, user, async_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Resume not found"
