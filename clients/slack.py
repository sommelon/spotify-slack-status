from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

import requests


class SlackApiClient:
    _headers = {
        "scheme": "https",
        "accept": "*/*",
        "origin": "https://app.slack.com",
        "accept-encoding": "gzip, deflate, br",
    }

    def __init__(self, token, d_cookie, workspace_domain):
        self.token = token
        self._d_cookie = d_cookie
        self.base_url = f"https://{workspace_domain}.slack.com/api"

    def update_user_status(
        self, text: str, emoji: str, expiration_time: datetime
    ) -> str:
        """Update and return the user status."""
        url = self.base_url + "/users.profile.set"

        expiration_timestamp = int(expiration_time.timestamp())
        profile_data = {
            "status_emoji": emoji,
            "status_expiration": expiration_timestamp,
            "status_text": text,
        }
        data = {
            "token": self.token,
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
        url = self.base_url + "/client.boot"

        data = {
            "token": self.token,
            "version": "5",
        }

        response = requests.request("POST", url, headers=self.headers, data=data)
        response.raise_for_status()
        json_response = response.json()
        self._handle_errors(json_response)

        return ClientBootResponse(
            status_text=json_response["profile"]["status_text"],
            status_emoji=json_response["profile"]["status_emoji"],
            status_expiration=json_response["profile"]["status_expiration"],
        )

    @property
    def headers(self):
        self._headers["cookie"] = self.d_cookie
        return self._headers

    @property
    def d_cookie(self):
        return f"d={self._d_cookie}; d-s={int(datetime.now().timestamp())}"

    def _handle_errors(self, json_response: dict):
        if "error" in json_response and json_response["error"] == "invalid_auth":
            raise SlackInvalidAuthError()


@dataclass
class ClientBootResponse:
    status_text: str
    status_emoji: str
    status_expiration: datetime = None

    def __post_init__(self):
        if self.status_expiration is None:
            self.status_expiration = datetime.fromtimestamp(self.timestamp)


class SlackInvalidAuthError(Exception):
    pass
