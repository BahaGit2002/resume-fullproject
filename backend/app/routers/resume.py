from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, swagger_auth
from app.models import User
from app.schemas.resume import (
    ResumeResponse, ResumeCreate, ResumeUpdate,
    ResumeImprove, ResumeHistoryResponse,
)
from app.schemas.user import UserResponse
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post(
    "/", response_model=ResumeResponse, status_code=201,
    dependencies=[Depends(swagger_auth)]
)
async def create_resume(
    resume_in: ResumeCreate, db: AsyncSession = Depends(get_db),
    user: UserResponse = Depends(get_current_user)
):
    return await ResumeService.create_resume(resume_in, db, user.id)


@router.get(
    "/", response_model=list[ResumeResponse], status_code=200,
    dependencies=[Depends(swagger_auth)]
)
async def get_resumes(
    db: AsyncSession = Depends(get_db),
    user: UserResponse = Depends(get_current_user)
):
    return await ResumeService.get_resumes(str(user.email), db)


@router.get(
    "/{resume_id}", response_model=ResumeResponse, status_code=200,
    dependencies=[Depends(swagger_auth)]
)
async def get_resume(
    resume_id: int, db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await ResumeService.get_resume(resume_id, current_user, db)


@router.put(
    "/{resume_id}", response_model=ResumeResponse, status_code=200,
    dependencies=[Depends(swagger_auth)]
)
async def update_resume(
    resume_id: int, resume_in: ResumeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await ResumeService.update_resume(
        resume_id, resume_in, db, current_user
    )


@router.delete(
    "/{resume_id}", status_code=204,
    dependencies=[Depends(swagger_auth)]
)
async def delete_resume(
    resume_id: int, db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ResumeService.delete_resume(resume_id, db, current_user)
    return


@router.post(
    "/{resume_id}/improve", response_model=ResumeImprove, status_code=200,
    dependencies=[Depends(swagger_auth)]
)
async def improve_resume(
    resume_id: int, resume_in: ResumeImprove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await ResumeService.improve_resume(
        resume_id, resume_in, db, current_user
    )


@router.get(
    "/{resume_id}/history", response_model=list[ResumeHistoryResponse],
    dependencies=[Depends(swagger_auth)]
)
async def get_resume_history(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ResumeService.get_resume_history(resume_id, current_user, db)
