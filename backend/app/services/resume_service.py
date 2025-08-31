from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.resume_repo import (
    ResumeRepository,
    ResumeHistoryRepository,
)
from app.repositories.user_repo import UserRepository
from app.schemas.resume import (
    ResumeCreate, ResumeResponse, ResumeUpdate,
    ResumeImprove, ResumeHistoryResponse,
)


class ResumeService:
    @staticmethod
    async def create_resume(
        resume_in: ResumeCreate, db: AsyncSession, user_id: int
    ) -> ResumeResponse:
        resume = await ResumeRepository(db).create(resume_in, user_id)
        return ResumeResponse.model_validate(resume)

    @staticmethod
    async def get_resumes(
        email: str, db: AsyncSession
    ) -> list[ResumeResponse]:
        user = await UserRepository(db).get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return [ResumeResponse.model_validate(resume) for resume in
                user.resumes]

    @staticmethod
    async def get_resume(
        resume_id: int, current_user: User, db: AsyncSession
    ) -> ResumeResponse:
        resume = await ResumeRepository(db).get_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if resume.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to access this resume"
            )

        return ResumeResponse.model_validate(resume)

    @staticmethod
    async def update_resume(
        resume_id: int,
        resume_in: ResumeUpdate,
        db: AsyncSession,
        current_user: User
    ) -> ResumeResponse:
        resume = await ResumeRepository(db).update(resume_id, resume_in)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if resume.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not allowed to edit this resume"
            )
        return ResumeResponse.model_validate(resume)

    @staticmethod
    async def delete_resume(
        resume_id: int, db: AsyncSession, current_user: User
    ):
        resume_repo = ResumeRepository(db)
        resume = await resume_repo.get_by_id(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        if resume.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not allowed to delete this resume"
            )

        await resume_repo.delete(resume_id)

    @staticmethod
    async def improve_resume(
        resume_id: int,
        resume_improve:
        ResumeImprove,
        db: AsyncSession,
        current_user: User
    ) -> ResumeImprove:
        resume_repo = ResumeRepository(db)
        resume = await resume_repo.get_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if resume.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not allowed to improve this resume"
            )

        improve_content = resume_improve.content + " [Improved]"
        resume_history_repo = ResumeHistoryRepository(db)
        new_version = await resume_history_repo.get_max_version(resume_id) + 1
        resume_history = await resume_history_repo.create(
            resume_id, improve_content, new_version
        )

        await resume_repo.update(
            resume_id, ResumeUpdate(
                title=resume.title, content=improve_content
            )
        )

        return ResumeImprove.model_validate(resume_history)

    @staticmethod
    async def get_resume_history(resume_id: int, current_user: User, db: AsyncSession) -> list[
        ResumeHistoryResponse]:
        resume = await ResumeRepository(db).get_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if resume.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not allowed to improve this resume"
            )

        return [ResumeHistoryResponse.model_validate(history) for history in
                resume.histories]
