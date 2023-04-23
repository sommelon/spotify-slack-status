import argparse
import os

TOKEN = os.getenv("TOKEN")
D_COOKIE = os.getenv("COOKIE")
EMOJI = os.getenv("EMOJI")
WORKSPACE_DOMAIN = os.getenv("WORKSPACE_DOMAIN")
REFRESH_INTERVAL = os.getenv("REFRESH_INTERVAL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default=TOKEN)
    parser.add_argument("--d-cookie", default=D_COOKIE)
    parser.add_argument("--refresh-interval", default=REFRESH_INTERVAL, type=int)
    parser.add_argument("--emoji", default=EMOJI)
    parser.add_argument("--workspace-domain", default=WORKSPACE_DOMAIN)
    parser.add_argument("--spotify-client-id", default=SPOTIFY_CLIENT_ID)
    parser.add_argument("--spotify-client-secret", default=SPOTIFY_CLIENT_SECRET)

    args = parser.parse_args()
    return args