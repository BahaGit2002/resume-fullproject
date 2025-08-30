from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Resume, ResumeHistory
from app.schemas.resume import ResumeCreate, ResumeUpdate


class ResumeRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, resume_in: ResumeCreate, user_id: int) -> Resume:
        resume = Resume(
            title=resume_in.title,
            content=resume_in.content,
            user_id=user_id,
        )
        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def get_by_id(self, ID: int) -> Resume | None:
        result = await self.db.execute(select(Resume).where(Resume.id == ID))
        return result.scalar_one_or_none()

    async def update(
        self, resume_id: int, resume_in: ResumeUpdate
    ) -> Resume | None:
        resume = await self.get_by_id(resume_id)
        if not resume:
            return None

        resume.title = resume_in.title
        resume.content = resume_in.content
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def delete(self, resume_id: int) -> Resume | None:
        resume = await self.get_by_id(resume_id)
        if not resume:
            return None

        await self.db.delete(resume)
        await self.db.commit()
        return resume


class ResumeHistoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_max_version(self, resume_id: int) -> int:
        result = await self.db.execute(
            select(ResumeHistory.version).where(
                ResumeHistory.resume_id == resume_id
            ).order_by(ResumeHistory.version.desc()).limit(1)
        )
        return result.scalar() or 0

    async def create(
        self, resume_id: int, content: str, new_version: int
    ) -> ResumeHistory:
        resume_history = ResumeHistory(
            resume_id=resume_id,
            content=content,
            version=new_version
        )
        self.db.add(resume_history)
        await self.db.commit()
        await self.db.refresh(resume_history)
        return resume_history
