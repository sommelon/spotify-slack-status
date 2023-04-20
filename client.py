from __future__ import annotations

import json
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional

import requests
from spotipy import Spotify


class SlackApiClient:
    headers = {
        "scheme": "https",
        "accept": "*/*",
        "origin": "https://app.slack.com",
        "accept-encoding": "gzip, deflate, br",
    }

    def __init__(self, token, d_cookie, workspace_domain, user_agent):
        self.token = token
        self.d_cookie = d_cookie
        self.headers[
            "cookie"
        ] = f"d={self.d_cookie}; d-s={int(datetime.now().timestamp())}"
        self.base_url = f"https://{workspace_domain}.slack.com/api"

    def update_status(self, text: str, emoji: str, expiration_time: datetime):
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
        return response.json()


class SpotifyApiClient(Spotify):
    def current_playback(self) -> Optional[Track]:
        try:
            current_track = super().current_playback()
        except Exception:
            current_track = super().current_playback()  # retry

        if (
            current_track is not None
            and "item" in current_track
            and current_track["is_playing"]
        ):
            track_name = current_track["item"]["name"]
            artist_name = current_track["item"]["artists"][0]["name"]
            duration = current_track["item"]["duration_ms"]
            progress = current_track["progress_ms"]
            track = Track(track_name, artist_name, progress, duration)
            return track


_Track = namedtuple("Track", "name,artist,progress_ms,duration_ms")


class Track(_Track):
    def get_track_endtime(self):
        remaining = self.duration_ms - self.progress_ms
        endtime = datetime.now() + timedelta(milliseconds=remaining)
        return endtime
