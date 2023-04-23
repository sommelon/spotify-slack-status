from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from logging import Logger

import requests


class SlackApiClient:
    _headers = {
        "scheme": "https",
        "accept": "*/*",
        "origin": "https://app.slack.com",
        "accept-encoding": "gzip, deflate, br",
    }

    def __init__(
        self, token: str, d_cookie: str, workspace_domain: str, logger: Logger
    ):
        self._token = token
        self._d_cookie = d_cookie
        self._base_url = f"https://{workspace_domain}.slack.com/api"
        self._logger = logger

    def clear_user_status(self):
        return self.update_user_status(None, None, None)

    def update_user_status(
        self, text: str, emoji: str, expiration_time: datetime
    ) -> str:
        """Update and return the user status."""
        url = self._base_url + "/users.profile.set"

        profile_data = {
            "status_emoji": emoji or "",
            "status_text": text or "",
        }
        if expiration_time:
            expiration_timestamp = int(expiration_time.timestamp())
            profile_data["status_expiration"] = expiration_timestamp

        data = {
            "token": self._token,
            "profile": json.dumps(profile_data),
            "_x_reason": "CustomStatusModal:handle_save",
            "_x_mode": "online",
            "_x_sonic": "true",
        }

        response = requests.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        json_response = response.json()
        self._handle_errors(json_response)

        return json_response["profile"]["status_text"]

    def get_user_status(self) -> ClientBootResponse:
        """Return the current user status"""
        url = self._base_url + "/client.boot"

        data = {
            "token": self._token,
            "version": "5",
        }

        response = requests.request("POST", url, headers=self.headers, data=data)
        response.raise_for_status()
        json_response = response.json()
        self._handle_errors(json_response)

        return ClientBootResponse(
            status_text=json_response["self"]["profile"]["status_text"] or None,
            status_emoji=json_response["self"]["profile"]["status_emoji"] or None,
            status_expiration=json_response["self"]["profile"]["status_expiration"]
            or None,
        )

    @property
    def headers(self):
        self._headers["cookie"] = self.d_cookie
        return self._headers

    @property
    def d_cookie(self):
        return f"d={self._d_cookie}; d-s={int(datetime.now().timestamp())}"

    def _handle_errors(self, json_response: dict):
        self._logger.debug(json_response)
        if "error" in json_response and json_response["error"] in [
            "invalid_auth",
            "not_authed",
        ]:
            raise SlackInvalidAuthError("Token or d-cookie invalid or expired.")


@dataclass
class ClientBootResponse:
    status_text: str
    status_emoji: str
    status_expiration: datetime = None

    def __post_init__(self):
        if isinstance(self.status_expiration, int):
            self.status_expiration = datetime.fromtimestamp(self.status_expiration)


class SlackInvalidAuthError(Exception):
    pass
