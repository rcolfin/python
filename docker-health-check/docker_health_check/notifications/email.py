from __future__ import annotations

import logging
import os
import smtplib
from email.message import EmailMessage
from typing import Final

from docker_health_check import constants, errors
from docker_health_check.settings import settings

logger = logging.getLogger(__name__)

IS_SUPPORTED: Final[bool] = bool(settings.email)


def send_mail(body: str) -> None:
    if settings.email is None:
        raise errors.EmailNotSupportedError

    msg = create_email_message(body)
    if msg is None:
        return

    logger.debug("Connecting to %s:%d", settings.email.host, settings.email.port)
    with smtplib.SMTP(settings.email.host, settings.email.port) as s:
        if settings.email.auth:
            logger.debug("Authenticating as %s", settings.email.auth.user)
            s.starttls()
            s.login(settings.email.auth.user, settings.email.auth.password)

        logger.info("Sending email:\n%s", msg)
        s.send_message(msg)


def create_email_message(body: str) -> EmailMessage | None:
    if settings.email is None:
        raise errors.EmailNotSupportedError

    assert settings.email.sender is not None
    assert settings.email.to is not None

    msg = EmailMessage()

    msg["Subject"] = os.path.expandvars(settings.email.subject)
    if any(ch in ("<", ">") for ch in settings.email.sender):
        msg["From"] = settings.email.sender
    else:
        msg["From"] = constants.SENDER_FMT.format(SENDER=settings.email.sender)

    if settings.email.to:
        msg["To"] = settings.email.to

    msg.set_content(body)
    return msg
