import asyncio
import logging
from collections.abc import AsyncIterable
from http import HTTPMethod
from typing import Any

from github import httpclient, providers

logger = logging.getLogger(__name__)


class GitHub(httpclient.HttpClient):
    def __init__(self, auth: providers.TokenProvider) -> None:
        super().__init__()
        self._token_provider = auth

    async def rerun(self, owner: str, repo: str, job_id: str) -> None:
        access_token = await self._token_provider.access_token()
        return await self._execute(
            HTTPMethod.GET,
            f"https://api.github.com/repos/{owner}/{repo}/actions/jobs/{job_id}/rerun",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    async def runs(self, owner: str, repo: str) -> AsyncIterable[dict[str, Any]]:
        access_token = await self._token_provider.access_token()
        runs = self._request(
            HTTPMethod.GET,
            f"https://api.github.com/repos/{owner}/{repo}/actions/runs",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        async for run in runs:
            yield run

    async def workflows(self, owner: str, repo: str) -> AsyncIterable[dict[str, Any]]:
        """
            List repository workflows

            Example Response:
            {
              "total_count": 2,
                "workflows": [
                {
                    "id": 161335,
                    "node_id": "MDg6V29ya2Zsb3cxNjEzMzU=",
                    "name": "CI",
                    "path": ".github/workflows/blank.yaml",
                    "state": "active",
                    "created_at": "2020-01-08T23:48:37.000-08:00",
                    "updated_at": "2020-01-08T23:50:21.000-08:00",
                    "url": "https://api.github.com/repos/octo-org/octo-repo/actions/workflows/161335",
                    "html_url": "https://github.com/octo-org/octo-repo/blob/master/.github/workflows/161335",
                    "badge_url": "https://github.com/octo-org/octo-repo/workflows/CI/badge.svg"
                },
                {
                    "id": 269289,
                    "node_id": "MDE4OldvcmtmbG93IFNlY29uZGFyeTI2OTI4OQ==",
                    "name": "Linter",
                    "path": ".github/workflows/linter.yaml",
                    "state": "active",
                    "created_at": "2020-01-08T23:48:37.000-08:00",
                    "updated_at": "2020-01-08T23:50:21.000-08:00",
                    "url": "https://api.github.com/repos/octo-org/octo-repo/actions/workflows/269289",
                    "html_url": "https://github.com/octo-org/octo-repo/blob/master/.github/workflows/269289",
                    "badge_url": "https://github.com/octo-org/octo-repo/workflows/Linter/badge.svg"
                }
            ]
        }
        """
        access_token = await self._token_provider.access_token()
        responses = self._request(
            HTTPMethod.GET,
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        async for response in responses:
            yield response

    async def jobs(self, owner: str, repo: str, run_id: str) -> AsyncIterable[dict[str, Any]]:
        access_token = await self._token_provider.access_token()
        responses = self._request(
            HTTPMethod.GET,
            f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        async for response in responses:
            yield response

    async def delete_run(self, run_url: str) -> None:
        access_token = await self._token_provider.access_token()
        return await self._execute(
            HTTPMethod.DELETE,
            run_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    async def delete_workflow_runs(self, owner: str, repo: str) -> None:
        runs = self.runs(owner, repo)
        tasks = []
        async for run in runs:
            for workflow_run in run["workflow_runs"]:
                url = workflow_run["url"]
                logger.info("Deleting %s", url)
                task = asyncio.ensure_future(self.delete_run(workflow_run["url"]))
                tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

    async def list_workflow_runs(self, owner: str, repo: str) -> None:
        runs = self.runs(owner, repo)
        async for run in runs:
            for workflow_run in run["workflow_runs"]:
                logger.info(
                    "%s %s %s\t%s\t%s",
                    workflow_run["created_at"],
                    workflow_run["status"],
                    workflow_run["id"],
                    workflow_run["name"],
                    workflow_run["url"],
                )
