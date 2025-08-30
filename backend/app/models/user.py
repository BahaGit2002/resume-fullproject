from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
