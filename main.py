import logging
import os
import time

from spotipy.oauth2 import SpotifyOAuth

from client import SlackApiClient, SpotifyApiClient

logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv("TOKEN")
D_COOKIE = os.getenv("COOKIE")
USER_AGENT = os.getenv("USER_AGENT")
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
slack = SlackApiClient(TOKEN, D_COOKIE, WORKSPACE_DOMAIN, USER_AGENT)


def update_status():
    track = spotify.current_playback()
    if track:
        response = slack.update_status(
            f"{track.name} by {track.artist}", EMOJI, track.get_track_endtime()
        )
        logging.info("Current status: " + response["profile"]["status_text"])
    else:
        logging.info("No song is currently playing on Spotify.")


try:
    update_status()

    while True:
        time.sleep(REFRESH_INTERVAL)
        update_status()
except Exception as e:
    logging.exception(str(e))
