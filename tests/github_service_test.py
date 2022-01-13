"""Testing for async github service classes."""

import json
import os
from unittest.mock import MagicMock
import jwt
import pytest
from thoth.investigator.github_service import GithubApp

PUBLICKEY_FILENAME = os.path.join(os.path.dirname(__file__), "keys/jwt-key.pub")
PRIVATEKEY_FILENAME = os.path.join(os.path.dirname(__file__), "keys/jwt-key")

GITHUBAPI_RESPONSES_DIR = os.path.join(os.path.dirname(__file__), "github_api_responses")


def _decrypt_jwt(jw_token: str, publickey):
    return jwt.decode(jwt=jw_token.encode(), key=publickey, algorithms=["RS256"])


async def get_json_file_content(file_name) -> dict:
    with open(file_name, "r") as f:
        return json.load(f)


class TestGithubApp:
    def setup(self):
        with open(PUBLICKEY_FILENAME, "r") as f:
            self.public_key = f.read()
        self.github_app = GithubApp("kebechet", PRIVATEKEY_FILENAME)

    def test_generate_jwt(self):
        jw_token = self.github_app._generate_jwt()
        content: dict = _decrypt_jwt(jw_token, self.public_key)
        assert content["iss"] == "kebechet"
        assert "iat" in content
        assert "exp" in content

    @pytest.mark.asyncio
    async def test_get_repo_installation_info(self):
        self.setup()
        mock = self.github_app._session
        mock.get = MagicMock()
        mock.get.return_value.__aenter__.return_value.json = lambda: get_json_file_content(
            os.path.join(GITHUBAPI_RESPONSES_DIR, "get_repo_installation_success.json")
        )
        mock.get.return_value.__aenter__.return_value.status = 200
        id = await self.github_app._get_installation_id_for_repo("github", "octocat")
        assert mock.get.call_count == 1
        assert id == 1

    @pytest.mark.asyncio
    async def test_get_repo_installation_token(self):
        self.setup()
        self.github_app._get_installation_id_for_repo = MagicMock()
        self.github_app._get_installation_id_for_repo.return_value = 1
        mock = self.github_app._session
        mock.post = MagicMock()
        mock.post.return_value.__aenter__.return_value.json = lambda: get_json_file_content(
            os.path.join(GITHUBAPI_RESPONSES_DIR, "get_installation_token_success.json")
        )
        mock.post.return_value.__aenter__.return_value.status = 201
        token = await self.github_app.get_repository_token("foo", "bar")
        assert token.token == "ghs_16C7e42F292c6912E7710c838347Ae178B4a"
