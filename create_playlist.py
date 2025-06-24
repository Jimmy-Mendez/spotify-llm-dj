import spotipy
from spotipy.oauth2 import SpotifyOAuth
from user_data import get_user_top_tracks
from llm_dj import prompt_llm, get_spotify_tracks
from dotenv import load_dotenv
import datetime

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read playlist-modify-public playlist-modify-private user-read-private"
))

def create_playlist(user_id, name, description="", public=False):
    """Create a new playlist for the user."""
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        collaborative=False,
        description=description
    )
    return playlist["id"], playlist["external_urls"]["spotify"]

def add_tracks_to_playlist(playlist_id, track_uris):
    """Add tracks to an existing playlist."""
    if not track_uris:
        raise ValueError("No valid tracks to add.")
    sp.playlist_add_items(playlist_id, track_uris)

if __name__ == "__main__":
    user_prompt = input("🎧 What's your vibe? → ")
    top_tracks = get_user_top_tracks()
    
    try:
        setlist = prompt_llm(user_prompt, top_tracks)
        setlist_spotify = get_spotify_tracks(setlist)
        track_uris = [track["uri"] for track in setlist_spotify]
        
        user_profile = sp.current_user()
        user_id = user_profile["id"]

        # Generate a playlist name
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        playlist_name = f"LLM DJ Set – {today}"
        playlist_desc = f'Vibe: "{user_prompt}"'

        # Create playlist + add tracks
        playlist_id, playlist_url = create_playlist(user_id, playlist_name, playlist_desc)
        add_tracks_to_playlist(playlist_id, track_uris)

        print("\n✅ Playlist created!")
        print(f"🎧 {playlist_name}: {playlist_url}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
