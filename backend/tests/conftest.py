import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession,
    async_sessionmaker,
)
from app.main import app
from app.database import get_db
from app.models import Resume, ResumeHistory, User
from app.models.base import Base
from httpx import AsyncClient, ASGITransport

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(engine):
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
async def clean_database(async_session: AsyncSession):
    """Фикстура для очистки базы данных перед каждым тестом."""
    await async_session.execute(delete(Resume))
    await async_session.execute(delete(ResumeHistory))
    await async_session.execute(delete(User))
    await async_session.commit()
    yield
