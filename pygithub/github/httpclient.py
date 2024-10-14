from __future__ import annotations

import logging
import re
from http import HTTPMethod, HTTPStatus
from typing import TYPE_CHECKING, Any, Final, Self, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

if TYPE_CHECKING:
    from collections.abc import Iterable
    from types import TracebackType

logger = logging.getLogger(__name__)
PAGINATION_LINK: Final[re.Pattern] = re.compile(r"<(?P<url>[^>]+)>;\s?rel=\"(?P<rel>[^\"]+)\"")


class HttpClient:
    def __init__(self) -> None:
        self._session: requests.Session | None = None

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: object,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session is not None:
            self._session.close()

    def _request(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> Iterable[dict[str, Any]]:
        next_url: str | None = url
        while next_url:
            r = self._make_request(method, next_url, headers, params=params)
            yield cast(dict[str, Any], r.json())
            next_url = self._get_next_pagination_link(r)

    @staticmethod
    def _get_next_pagination_link(response: requests.Response) -> str | None:
        link = response.headers.get("Link")
        if link is None:
            return None
        for m in PAGINATION_LINK.finditer(link):
            if m.groups()[1] == "next":
                return m.groups()[0]
        return None

    def _execute(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> None:
        r = self._make_request(method, url, headers, params=params)
        assert r.status_code == HTTPStatus.NO_CONTENT

    def _make_request(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> requests.Response:
        logger.debug("Sending %s request to %s", method, url)
        r = self._ensure_session().request(method, url, headers=headers, params=params)
        r.raise_for_status()
        return r

    def _ensure_session(self) -> requests.Session:
        if self._session is None:
            self._session = self._create_session()
        return self._session

    def _create_session(self, retry_count: int = 3) -> requests.Session:
        s = requests.Session()
        s.headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        retries = Retry(
            total=retry_count,
            backoff_factor=0.1,
        )
        adapter = HTTPAdapter(max_retries=retries)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        return s
