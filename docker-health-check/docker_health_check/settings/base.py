from __future__ import annotations

from pydantic_settings import BaseSettings

from docker_health_check.settings.email import EmailSettings  # noqa: TCH001


class Settings(BaseSettings):
    email: EmailSettings | None = None

    class Config:
        env_nested_delimiter = "__"


settings = Settings()
