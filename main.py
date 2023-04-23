import logging
import time

from spotipy.oauth2 import SpotifyOAuth

from args import parse_args
from clients.slack import SlackApiClient
from clients.spotify import SpotifyApiClient

logging.basicConfig(level=logging.INFO)


def run(args):
    spotify = SpotifyApiClient(
        auth_manager=SpotifyOAuth(
            client_id=args.spotify_client_id,
            client_secret=args.spotify_client_secret,
            redirect_uri="http://localhost:8000",
            scope="user-read-playback-state",
        )
    )
    slack = SlackApiClient(args.token, args.d_cookie, args.workspace_domain)

    def update_user_status():
        track = spotify.current_playback()
        if track:
            status = slack.update_user_status(
                f"{track.name} by {track.artist}", args.emoji, track.get_track_endtime()
            )
            logging.info("Current status: " + status)
        else:
            logging.info("No song is currently playing on Spotify.")

    try:
        update_user_status()

        while True:
            time.sleep(args.refresh_interval)
            update_user_status()
    except Exception as e:
        logging.exception(str(e))


if __name__ == "__main__":
    args = parse_args()
    run(args)
