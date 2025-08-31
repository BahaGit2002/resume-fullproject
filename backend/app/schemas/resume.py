from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class ResumeCreate(BaseModel):
    title: str
    content: str


class ResumeImprove(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, strict=True)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
