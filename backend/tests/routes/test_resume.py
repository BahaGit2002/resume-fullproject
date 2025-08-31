import pytest
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Resume, ResumeHistory
from app.models.user import User
from app.schemas.resume import ResumeCreate
from app.core.security import create_jwt
from app.services.resume_service import ResumeService


@pytest.fixture
async def auth_header(async_session: AsyncSession):
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    token = create_jwt({"sub": user.email})
    return {"Authorization": f"Bearer {token}"}, user


@pytest.mark.asyncio
async def test_create_resume(
    client: AsyncClient, async_session: AsyncSession, auth_header
):
    headers, user = auth_header
    data = {"title": "Test Resume", "content": "Sample content"}

    response = await client.post("/resumes/", json=data, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Test Resume"
    assert body["content"] == "Sample content"
    assert body["user_id"] == user.id


@pytest.mark.asyncio
async def test_get_resumes(
    client: AsyncClient, async_session: AsyncSession, auth_header
):
    headers, user = auth_header
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    result = await async_session.execute(
        select(Resume).where(Resume.id == resume.id)
    )
    db_resume = result.unique().scalar_one_or_none()
    assert db_resume is not None, "Resume was not saved to the database"
    assert db_resume.user_id == user.id, "Resume user_id does not match"

    response = await client.get("/resumes/", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)


@pytest.mark.asyncio
async def test_get_resume(
    client: AsyncClient, async_session: AsyncSession, auth_header
):
    headers, user = auth_header
    resume_in = ResumeCreate(title="Test Resume", content="Sample content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    response = await client.get(f"/resumes/{resume.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == resume.id
    assert body["title"] == resume.title


@pytest.mark.asyncio
async def test_update_resume(
    client: AsyncClient, async_session: AsyncSession, auth_header
):
    headers, user = auth_header
    resume_in = ResumeCreate(title="Old Resume", content="Old content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    update_data = {"title": "Updated Resume", "content": "Updated content"}
    response = await client.put(
        f"/resumes/{resume.id}", json=update_data, headers=headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated Resume"
    assert body["content"] == "Updated content"


@pytest.mark.asyncio
async def test_delete_resume(
    client: AsyncClient, async_session: AsyncSession, auth_header
):
    headers, user = auth_header
    resume_in = ResumeCreate(title="To Delete", content="To Delete content")
    resume = await ResumeService.create_resume(
        resume_in, async_session, user.id
    )

    response = await client.delete(
        f"/resumes/{resume.id}", headers=headers
    )
    assert response.status_code == 204

    response = await client.get(f"/resumes/{resume.id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_improve_resume(client: AsyncClient, async_session: AsyncSession, auth_header):
    headers, user = auth_header
    resume_in = ResumeCreate(title="To Improve", content="Initial content")
    resume = await ResumeService.create_resume(resume_in, async_session, user.id)
    await async_session.commit()

    result = await async_session.execute(select(Resume).where(Resume.id == resume.id))
    db_resume = result.unique().scalar_one_or_none()
    assert db_resume is not None, f"Resume with ID {resume.id} was not found in the database"
    assert db_resume.user_id == user.id, f"Resume user_id {db_resume.user_id} does not match user {user.id}"

    response = await client.post(
        f"/resumes/{resume.id}/improve",
        json={"content": "Improved content"},
        headers=headers
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    body = response.json()
    assert "Improved" in body["content"]
