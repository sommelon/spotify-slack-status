import logging
import time

from spotipy.oauth2 import SpotifyOAuth

from args import parse_args
from clients.slack import SlackApiClient, SlackInvalidAuthError
from clients.spotify import SpotifyApiClient

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
            logger.info(str(e), "To continue, re-enter the credentials.")
            token, d_cookie = self._ask_for_slack_credentials()
            self._slack = SlackApiClient(token, d_cookie, self._args.workspace_domain)
        except Exception as e:
            logger.exception(str(e))

    def _update_user_status(self):
        track = self._spotify.current_playback()
        if not track:
            logger.info("No song is currently playing on Spotify.")

        response = self._slack.get_user_status()

        new_status = f"{track.name} by {track.artist}" if track else None
        if response.status_text == new_status:
            if new_status:
                logger.debug("Status already set")
            return

        if response.status_emoji is None and track is None:
            logger.debug("Nothing to update")
            return
        elif response.status_emoji and response.status_emoji != self._args.emoji:
            logger.info(
                "Slack status not updated, because it would override a possibly more important status."
            )
            return

        if track:
            status = self._slack.update_user_status(
                new_status,
                self._args.emoji,
                track.get_track_endtime(),
            )
            logger.info("Current status: " + status)
        else:
            status = self._slack.clear_user_status()
            logger.info("Cleared status.")

    @staticmethod
    def _ask_for_slack_credentials():
        token = input("Slack token: ")
        d_cookie = input("Slack d-cookie: ")
        return token, d_cookie


if __name__ == "__main__":
    args = parse_args()
    StatusUpdater(args).run()
