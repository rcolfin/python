from __future__ import annotations

from typing import Self

from pydantic import BaseModel, Field, model_validator


class EmailAuth(BaseModel):
    user: str = Field(title="The server authentication user")
    password: str = Field(title="The server authentication password")


class EmailSettings(BaseModel):
    sender: str | None = Field(None, title="The email sender")
    to: str | None = Field(None, title="The recipient or recipients separated by comma")
    subject: str = Field("Docker Health Check updates on $HOSTNAME", title="The subject of the email")
    host: str = Field("localhost", title="The SMTP server host")
    port: int = Field(587, title="The SMTP server port")
    auth: EmailAuth | None = None

    @model_validator(mode="after")  # type: ignore  # noqa: PGH003
    def _validate(self) -> Self | None:
        if self.sender is None or self.to is None:
            return None
        return self
