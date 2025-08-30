from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(resume_router, prefix="/resumes", tags=["resumes"])
