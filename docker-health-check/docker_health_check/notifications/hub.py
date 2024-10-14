import logging
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from queue import Queue
from types import TracebackType
from typing import Self

from tabulate import tabulate

from docker_health_check import constants
from docker_health_check.notifications import email

logger = logging.getLogger(__name__)


class NotificationHub:
    def __init__(self) -> None:
        self._events: Queue[tuple[datetime, str]] = Queue()
        if self.is_supported:
            logger.info("Notifications are enabled.")

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: object,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @contextmanager
    def notify_onexit(self) -> Iterator[None]:
        """Notifies when the context manager closes."""
        try:
            yield
        finally:
            self.notify()

    @property
    def is_supported(self) -> bool:
        return email.IS_SUPPORTED

    def close(self) -> None:
        self._events.shutdown()

    def enqueue(self, event: str) -> None:
        if not self.is_supported:
            return
        self._events.put_nowait((datetime.now(tz=UTC), event))

    def notify(self) -> None:
        if not self.is_supported:
            return

        events = self._get_events()
        if not events:
            logger.debug("No events to raise.")
            return

        body = tabulate(
            ((timestamp.strftime(constants.DATETIME_FMT), msg) for (timestamp, msg) in events),
            headers=["TIMESTAMP", "MESSAGE"],
        )

        email.send_mail(body)

    def _get_events(self) -> list[tuple[datetime, str]]:
        events: list[tuple[datetime, str]] = []
        while self._events.qsize():
            events.append(self._events.get_nowait())
        events.sort(key=lambda x: x[0])
        return events
