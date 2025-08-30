from pydantic import BaseModel, ConfigDict


class ResumeCreate(BaseModel):
    title: str
    content: str


class ResumeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class ResumeResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ResumeHistoryResponse(BaseModel):
    id: int
    resume_id: int
    version: int
    content: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
