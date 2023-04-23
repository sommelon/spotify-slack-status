import logging
import time

from spotipy.oauth2 import SpotifyOAuth

from args import parse_args
from clients.slack import SlackApiClient, SlackInvalidAuthError
from clients.spotify import SpotifyApiClient

logging.basicConfig(level=logging.INFO)


class StatusUpdater:
    def __init__(self, args):
        self._args = args
        self._spotify = SpotifyApiClient(
            auth_manager=SpotifyOAuth(
                client_id=args.spotify_client_id,
                client_secret=args.spotify_client_secret,
                redirect_uri="http://localhost:8000",
                scope="user-read-playback-state",
            )
        )
        self._slack = SlackApiClient(args.token, args.d_cookie, args.workspace_domain)

    def run(self):
        try:
            self._update_user_status()

            while True:
                time.sleep(self._args.refresh_interval)
                self._update_user_status()
        except SlackInvalidAuthError as e:
            print(str(e), "To continue, re-enter the credentials.")
            token, d_cookie = self._ask_for_slack_credentials()
            self._slack = SlackApiClient(token, d_cookie, self._args.workspace_domain)
        except Exception as e:
            logging.exception(str(e))

    def _update_user_status(self):
        track = self._spotify.current_playback()
        if track:
            status = self._slack.update_user_status(
                f"{track.name} by {track.artist}",
                self._args.emoji,
                track.get_track_endtime(),
            )
            logging.info("Current status: " + status)
        else:
            logging.info("No song is currently playing on Spotify.")

    @staticmethod
    def _ask_for_slack_credentials():
        token = input("Slack token: ")
        d_cookie = input("Slack d-cookie: ")
        return token, d_cookie


if __name__ == "__main__":
    args = parse_args()
    StatusUpdater(args).run()
