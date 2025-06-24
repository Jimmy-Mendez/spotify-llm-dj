import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read playlist-modify-public playlist-modify-private user-read-private"
))

def get_user_top_tracks(limit=20, time_range="medium_term"):
    top = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [{
        "name": t["name"],
        "artist": t["artists"][0]["name"],
        "id": t["id"]
    } for t in top["items"]]

if __name__ == "__main__":
    print(json.dumps(get_user_top_tracks(), indent=2))

