from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from docker_health_check.settings.email import EmailSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    email: EmailSettings | None = None


settings = Settings()
