from __future__ import annotations

from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional

from spotipy import Spotify


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
