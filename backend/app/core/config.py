from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int
    ALGORITHM: str
    BACKEND_CORS_ORIGINS: list[str] = [""]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
