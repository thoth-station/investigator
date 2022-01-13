#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2022 Kevin Postlethwait
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""This is an async library for interacting with the Github API using aiohttp."""

from typing import Optional, Union, NamedTuple
import asyncio
import time
from datetime import datetime

import aiohttp
import jwt

# this is an async wrapper for the GitHub API a more feature rich library is
# available here, but it is unclear whether this project is stable.
# https://github.com/brettcannon/gidgethub/issues


BASE_API_URL = "https://api.github.com"


class InstallationNotFoundError(Exception):
    """Raised on http auth errors when the service is not installed on the requested repo."""

    pass


class UnknownResponseCodeError(Exception):
    """Raised when aiohttp request returns with status that is not handled."""

    pass


class AccessToken(NamedTuple):
    """Generic access token representation."""

    token: str
    expiration: Optional[Union[int, float]] = None  # epoch time


class GithubAuth:
    """Authorization interface."""

    def __init__(self):
        """Create generic github auth object."""
        self._event_loop = asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(
            loop=self._event_loop, headers={"Accept": "application/vnd.github.v3"}  # current API version
        )

    def __del__(self):
        """Close aiohttp session associated with the object."""
        self._event_loop.run_until_complete(self._session.close())

    async def get_auth_token(self):
        """Get auth token for interacting with github api."""
        raise NotImplementedError()

    async def get_repository_token(self, namespace, repo) -> AccessToken:
        """Get auth token for interacting with a specific repository."""
        raise NotImplementedError()


class GithubOAuth(GithubAuth):
    """Implementation of GithubAuth using an OAuth token."""

    def __init__(self, token: str):
        """Github auth which uses simple OAuth token authentication."""
        self._token = AccessToken(token=token, expiration=None)
        super().__init__()

    async def get_auth_token(self):
        """Return OAuth token for authorization."""
        return self._token

    async def get_repository_token(self, namespace, repo) -> AccessToken:
        """Return OAuthToken for authorization."""
        del namespace, repo  # unused for this implementation
        return self._token


class GithubApp(GithubAuth):
    """Implementation of GithubAuth using github app."""

    def __init__(self, app_id, app_private_key_path: str):
        """Return GitHubAuth instance for a GitHub application."""
        self.app_private_key = self._get_app_private_key(app_private_key_path)
        self.app_id = app_id
        super().__init__()

    def _generate_jwt(self):
        payload = {
            # issued at time, 60 seconds in the past to allow for clock drift
            "iat": int(time.time()) - 60,
            # JWT expiration time (1 minute)
            "exp": int(time.time()) + 60,
            # GitHub App's identifier
            "iss": self.app_id,
        }
        encrypted = jwt.encode(payload, self.app_private_key, algorithm="RS256")
        if isinstance(encrypted, bytes):
            encrypted = encrypted.decode("utf-8")
        return encrypted

    @staticmethod
    def _get_app_private_key(private_key_path: str) -> str:
        """
        Get private key string from file.

        Returns
            str: PEM256 key found in private_key_path file
        Raises
            FileNotFoundError
        """
        with open(private_key_path, "r") as f:
            return f.read()

    async def get_auth_token(self):
        """
        Get App auth token.

        Note
            expires in 60s it is best to generate a new token for each request
        """
        return AccessToken(token=self._generate_jwt(), expiration=int(time.time()) + 60)

    async def _get_repository_installation(self, namespace, repo):
        """https://docs.github.com/en/rest/reference/apps#get-a-repository-installation-for-the-authenticated-app."""
        async with self._session.get(
            f"{BASE_API_URL}/repos/{namespace}/{repo}/installation",
            headers={"Authorization": f"Bearer {(await self.get_auth_token()).token}"},
        ) as r:
            if r.status == 404:
                raise InstallationNotFoundError(f"App not installed for {namespace}/{repo}.")
            elif r.status == 200:
                return await r.json()
            else:  # only other response type is 301-'Moved Permanently' which should automatically redirect
                raise UnknownResponseCodeError(f"GitHub API responded with status: {r.status}")

    async def _get_installation_id_for_repo(self, namespace, repo):
        """Return the installation id for a given repository.

        Returns:
            int: id of installation
        Raises:
            InstallationNotFoundError
        """
        installation_info = await self._get_repository_installation(namespace, repo)
        return installation_info["id"]

    async def get_repository_token(self, namespace, repo, installation_id: Optional[int] = None) -> AccessToken:
        """
        Get auth token for a specific repository. Resultant token can be used for the github API Authorization header.

        args: namespace (str): user or organization which owns the repository repo (str): the name of the repository
            without the attached namespace
        raises: UnknownResponseCodeError, aiohttp.ClientResponseError
        """
        installation_id = self._get_installation_id_for_repo(namespace, repo)
        async with self._session.post(
            f"{BASE_API_URL}/app/installations/{installation_id}/access_tokens",
            headers={"Authorization": f"Bearer {(await self.get_auth_token()).token}"},
            raise_for_status=True,
        ) as r:
            if r.status == 201:  # Successfully created
                r_dict = await r.json()
                return AccessToken(
                    r_dict["token"], datetime.strptime(r_dict["expires_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
                )
            else:
                raise UnknownResponseCodeError(f"Unknown response code {r.status} while retrieving repository token")


class GithubService:
    """Async class for interacting with generic GithubApi."""

    def __init__(
        self, token: Optional[str] = None, app_id: Optional[str] = None, app_private_key_path: Optional[str] = None
    ):
        """Return instance of GithubService."""
        if app_private_key_path and app_id:
            self._auth: GithubAuth = GithubApp(app_id=app_id, app_private_key_path=app_private_key_path)
        elif token:
            self._auth = GithubOAuth(token=token)

    def get_project(self, namespace, repo):
        """Return instance of a GitHubProject."""
        return GithubProject(self, namespace, repo)


class GithubProject:
    """Async class for interacting with GitHub repository API."""

    def __init__(
        self,
        github_service: GithubService,
        namespace: str,
        repo: str,
        repository_id: Optional[int] = None,
    ):
        """Return an instance of a GithubProject."""
        self._repository_id = repository_id  # for cases where we already have the repo_id to minimize api calls
        self._github_service = github_service
        self.namespace = namespace
        self.repo = repo
        self._token: Optional[AccessToken] = None

    async def _get_token(self) -> str:
        if self._token is None:
            self._token = await self._github_service._auth.get_repository_token(self.namespace, self.repo)
        elif self._token.expiration is not None and self._token.expiration - time.time() < 0:  # refresh token
            self._token = await self._github_service._auth.get_repository_token(self.namespace, self.repo)
        return self._token.token

    async def get_file(self, file_path: str) -> str:
        """
        Download GitHub file to given path.

        args:
            file_path (str): path to file relative to the root of the git repository
        returns:
            str
        raises:
            FileNotFoundError, TypeError, aiohttp.ClientResponseError
        GitHubAPI docs:
            https://docs.github.com/en/rest/reference/repos#get-repository-content
        """
        async with self._github_service._auth._session.get(
            f"{BASE_API_URL}/repos/{self.namespace}/{self.repo}/contents/{file_path}",
            headers={"Authorization": f"token {await self._get_token()}"},
        ) as r:
            if r.status == 404:
                raise FileNotFoundError(f"{self.namespace}/{self.repo} does not have {file_path}")
            elif r.status == 200:
                r_dict = await r.json()
                if type(r_dict) == list:
                    raise TypeError(f"{self.namespace}/{self.repo} has {file_path} but it is a directory")
                if r_dict["type"] != "file":
                    raise TypeError(f"{self.namespace}/{self.repo} has {file_path} but it is a {r_dict['type']}")
                download_url = r_dict["download_url"]
                async with self._github_service._auth._session.get(
                    download_url, headers={"Authorization": f"token {await self._get_token()}"}
                ) as r2:
                    if r2.status == 200:
                        return (await r2.read()).decode("utf8")
                    else:
                        raise UnknownResponseCodeError(
                            f"Unknown response code, {r.status}, when downloading file from git"
                        )
            else:
                r.raise_for_status()
                raise UnknownResponseCodeError(f"github api responded with status code {r.status} which is not handled")
