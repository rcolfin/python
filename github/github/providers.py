from __future__ import annotations

import abc
import logging
import time
from datetime import timedelta
from http import HTTPMethod
from typing import TYPE_CHECKING, Any, Final, cast

import jwt

from github.httpclient import HttpClient

if TYPE_CHECKING:
    from collections.abc import AsyncIterable

logger = logging.getLogger(__name__)


class TokenProvider(abc.ABC):
    @abc.abstractmethod
    async def access_token(self) -> str:
        pass


class Token(TokenProvider):
    def __init__(self, access_token: str) -> None:
        super().__init__()
        self._access_token = access_token

    async def access_token(self) -> str:
        return self._access_token


class Application(TokenProvider, HttpClient):
    MIN_EXPIRATION: Final[timedelta] = timedelta()
    MAX_EXPIRATION: Final[timedelta] = timedelta(minutes=10)
    EXPIRATION_OFFSET: Final[timedelta] = timedelta(minutes=1)
    JWT_ALGORITHM: Final[str] = "RS256"

    def __init__(
        self,
        client_id: str,
        signing_key: bytes,
        installation_id: str | None = None,
        expiration: timedelta = timedelta(minutes=9, seconds=50),
    ) -> None:
        """
        Args:
            client_id (str): GitHub App's client ID
            signing_key (bytes): The bytes containing the RS256 key.
            installation_id (str): The GitHub App's Installation ID.
            expiration (timedelta): The expiration time of the JWT, after which it
                can't be used to request an installation token. The time must be
                no more than 10 minutes into the future.
        """
        super().__init__()
        assert self.MIN_EXPIRATION < expiration < self.MAX_EXPIRATION

        self._client_id = client_id
        self._installation_id = installation_id
        self._signing_key = signing_key
        self._expiration = expiration
        self._access_token: tuple[str, int] | None = None

    async def access_token(self) -> str:
        """
        Gets the access token.

        Returns:
            jwt_token (str): The JWT token
        """
        if self._access_token is None or self._access_token[1] <= time.time():
            self._access_token = await self._query_access_token()

        return self._access_token[0]

    async def get_app(self) -> dict[str, Any]:
        """Gets the authenticated app."""
        jwt_token = self.generate_jwt()
        responses = self._request(
            HTTPMethod.GET, "https://api.github.com/app", headers={"Authorization": f"Bearer {jwt_token}"}
        )
        async for response in responses:
            return response
        return {}

    async def get_app_installations(self) -> AsyncIterable[dict[str, Any]]:
        jwt_token = self.generate_jwt()
        responses = self._request(
            HTTPMethod.GET,
            "https://api.github.com/app/installations",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        async for response in responses:
            yield response

    def generate_jwt(self) -> str:
        """
        Creates a JWT from the client id and signing key.

        Returns:
            jwt_token (str): The JWT token
        """
        iat = int(time.time())
        exp = iat + int(self._expiration.total_seconds())
        payload = {"iat": iat, "exp": exp, "iss": self._client_id}

        # Create JWT
        encrypted: str | bytes = jwt.encode(payload, self._signing_key, algorithm=self.JWT_ALGORITHM)
        if isinstance(encrypted, bytes):
            return encrypted.decode("utf-8")

        return cast(str, encrypted)

    async def _query_access_token(self) -> tuple[str, int]:
        assert self._installation_id is not None, "installation_id is not set"

        jwt_token = self.generate_jwt()
        responses = self._request(
            HTTPMethod.POST,
            f"https://api.github.com/app/installations/{self._installation_id}/access_tokens",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )

        async for response in responses:
            token = cast(str, response["token"])
            exp = int(time.time() + self._expiration.total_seconds() - self.EXPIRATION_OFFSET.total_seconds())
            return token, exp

        return "", 0
