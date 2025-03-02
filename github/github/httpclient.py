from __future__ import annotations

import logging
import re
from contextlib import asynccontextmanager
from http import HTTPMethod, HTTPStatus
from typing import TYPE_CHECKING, Any, Final, Self, cast

import aiohttp
import backoff

from github import constants

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, AsyncIterable
    from types import TracebackType

logger = logging.getLogger(__name__)
PAGINATION_LINK: Final[re.Pattern] = re.compile(r"<(?P<url>[^>]+)>;\s?rel=\"(?P<rel>[^\"]+)\"")


class HttpClient:
    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: object,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        await self.close()
        return False

    async def close(self) -> Self:
        if self._session is None:
            return self
        await self._session.close()
        return self

    async def _request(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> AsyncIterable[dict[str, Any]]:
        next_url: str | None = url
        while next_url:
            async with self._make_request(method, next_url, headers, params=params) as response:
                yield cast("dict[str, Any]", await response.json())
                next_url = self._get_next_pagination_link(response)

    @staticmethod
    def _get_next_pagination_link(response: aiohttp.ClientResponse) -> str | None:
        link = response.headers.get("Link")
        if link is None:
            return None
        for m in PAGINATION_LINK.finditer(link):
            if m.groups()[1] == "next":
                return m.groups()[0]
        return None

    async def _execute(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> None:
        async with self._make_request(method, url, headers, params=params) as response:
            assert response.status == HTTPStatus.NO_CONTENT

    @backoff.on_exception(
        backoff.expo, aiohttp.ClientError, max_tries=constants.MAX_RETRIES, max_time=constants.MAX_RETRY_TIME
    )
    @asynccontextmanager
    async def _make_request(
        self, method: HTTPMethod, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        session = self._ensure_session()
        async with session.request(method, url, headers=headers, params=params, raise_for_status=True) as response:
            yield response

    def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = self._create_session()
        return self._session

    def _create_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        )
