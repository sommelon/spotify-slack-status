import logging
import os
import time

from spotipy.oauth2 import SpotifyOAuth

from clients.slack import SlackApiClient
from clients.spotify import SpotifyApiClient

logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv("TOKEN")
D_COOKIE = os.getenv("COOKIE")
REFRESH_INTERVAL = os.getenv("REFRESH_INTERVAL")
EMOJI = os.getenv("EMOJI")
WORKSPACE_DOMAIN = os.getenv("WORKSPACE_DOMAIN")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL"))
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify = SpotifyApiClient(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://localhost:8000",
        scope="user-read-playback-state",
    )
)
slack = SlackApiClient(TOKEN, D_COOKIE, WORKSPACE_DOMAIN)


def update_user_status():
    track = spotify.current_playback()
    if track:
        status = slack.update_user_status(
            f"{track.name} by {track.artist}", EMOJI, track.get_track_endtime()
        )
        logging.info("Current status: " + status)
    else:
        logging.info("No song is currently playing on Spotify.")


try:
    update_user_status()

    while True:
        time.sleep(REFRESH_INTERVAL)
        update_user_status()
except Exception as e:
    logging.exception(str(e))
