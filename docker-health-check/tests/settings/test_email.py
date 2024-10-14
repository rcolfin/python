import os
from typing import Final
from unittest import mock

EMAIL__SENDER: Final[str] = "from@gmail.com"
EMAIL__TO: Final[str] = "to@gmail.com"
EMAIL__SUBJECT: Final[str] = "This is a test subject"
EMAIL__HOST: Final[str] = "smtp.gmail.com"
EMAIL__PORT: Final[int] = 587
EMAIL__AUTH__USER: Final[str] = "test_user"
EMAIL__AUTH__PASSWORD: Final[str] = "test_password"


@mock.patch.dict(
    os.environ,
    {
        "EMAIL__SENDER": EMAIL__SENDER,
        "EMAIL__TO": EMAIL__TO,
        "EMAIL__SUBJECT": EMAIL__SUBJECT,
        "EMAIL__HOST": EMAIL__HOST,
        "EMAIL__PORT": str(EMAIL__PORT),
        "EMAIL__AUTH__USER": EMAIL__AUTH__USER,
        "EMAIL__AUTH__PASSWORD": EMAIL__AUTH__PASSWORD,
    },
    clear=True,
)
def test_email_message_with_auth() -> None:
    from docker_health_check.settings.base import Settings

    settings = Settings()
    email_settings = settings.email
    assert email_settings is not None
    assert email_settings.auth is not None
    assert email_settings.host == EMAIL__HOST
    assert email_settings.port == EMAIL__PORT
    assert email_settings.to == EMAIL__TO
    assert email_settings.sender == EMAIL__SENDER
    assert email_settings.subject == EMAIL__SUBJECT
    assert email_settings.auth.user == EMAIL__AUTH__USER
    assert email_settings.auth.password == EMAIL__AUTH__PASSWORD


@mock.patch.dict(
    os.environ,
    {
        "EMAIL__SENDER": EMAIL__SENDER,
        "EMAIL__TO": EMAIL__TO,
        "EMAIL__SUBJECT": EMAIL__SUBJECT,
        "EMAIL__HOST": EMAIL__HOST,
        "EMAIL__PORT": str(EMAIL__PORT),
    },
    clear=True,
)
def test_email_message_without_auth() -> None:
    from docker_health_check.settings.base import Settings

    settings = Settings()
    email_settings = settings.email
    assert email_settings is not None
    assert email_settings.auth is None


@mock.patch.dict(
    os.environ,
    {
        "EMAIL__SENDER": EMAIL__SENDER,
        "EMAIL__SUBJECT": EMAIL__SUBJECT,
        "EMAIL__HOST": EMAIL__HOST,
        "EMAIL__PORT": str(EMAIL__PORT),
    },
    clear=True,
)
def test_email_settings_not_created_on_missing_required_fields() -> None:
    from docker_health_check.settings.base import Settings

    settings = Settings()
    email_settings = settings.email
    assert email_settings is None


@mock.patch.dict(
    os.environ,
    {
        "EMAIL__TO": EMAIL__TO,
        "EMAIL__SUBJECT": EMAIL__SUBJECT,
        "EMAIL__HOST": EMAIL__HOST,
        "EMAIL__PORT": str(EMAIL__PORT),
    },
    clear=True,
)
def test_email_settings_not_created_on_missing_required_fields2() -> None:
    from docker_health_check.settings.base import Settings

    settings = Settings()
    email_settings = settings.email
    assert email_settings is None
