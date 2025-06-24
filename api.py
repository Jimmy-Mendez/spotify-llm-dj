from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import datetime
from create_playlist import create_playlist, add_tracks_to_playlist
from user_data import get_user_top_tracks
from llm_dj import prompt_llm, get_spotify_tracks

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    """Serve the frontend HTML."""
    return FileResponse("static/index.html")

sp_oauth = SpotifyOAuth(
    scope="user-top-read playlist-modify-public playlist-modify-private user-read-private",
    open_browser=False
)


@app.get("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return {"auth_url": auth_url}

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        raise HTTPException(status_code=400, detail="Failed to get token")
    return RedirectResponse(url="/")


@app.post("/playlist")
def make_playlist(vibe: str):
    if not vibe:
        raise HTTPException(status_code=400, detail="Vibe required")
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise HTTPException(status_code=401, detail="Not authenticated")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = get_user_top_tracks()
    setlist = prompt_llm(vibe, top_tracks)
    setlist_spotify = get_spotify_tracks(setlist)
    track_uris = [t['uri'] for t in setlist_spotify]
    user_profile = sp.current_user()
    user_id = user_profile['id']
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    playlist_name = f"LLM DJ Set – {today}"
    playlist_desc = f'Vibe: "{vibe}"'
    playlist_id, playlist_url = create_playlist(user_id, playlist_name, playlist_desc)
    add_tracks_to_playlist(playlist_id, track_uris)
    return {"playlist_url": playlist_url}

@app.get("/profile")
def profile():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise HTTPException(status_code=401, detail="Not authenticated")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_user()
