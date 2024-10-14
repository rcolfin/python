from typing import Final
from unittest import mock

import pytest

from docker_health_check import constants, errors
from docker_health_check.notifications import email
from docker_health_check.settings.base import Settings
from docker_health_check.settings.email import EmailSettings

EMAIL__SENDER: Final[str] = "from@gmail.com"
EMAIL__TO: Final[str] = "to@gmail.com"
EMAIL__SUBJECT: Final[str] = "This is a test subject"


def test_email_message() -> None:
    email_settings = EmailSettings(sender=EMAIL__SENDER, to=EMAIL__TO, subject=EMAIL__SUBJECT)
    settings = Settings(email=email_settings)
    with mock.patch("docker_health_check.notifications.email.settings", settings):
        msg = email.create_email_message("test")
        assert msg is not None
        assert msg["Subject"] == EMAIL__SUBJECT
        assert msg["From"] == constants.SENDER_FMT.format(SENDER=EMAIL__SENDER)
        assert msg["To"] == EMAIL__TO


def test_email_message_returns_none_on_no_email_settings() -> None:
    settings = Settings(email=None)
    with mock.patch("docker_health_check.notifications.email.settings", settings), pytest.raises(errors.EmailNotSupportedError):
        email.create_email_message("test")
