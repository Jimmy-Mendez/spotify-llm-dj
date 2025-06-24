from openai import OpenAI
import json
import spotipy
from user_data import get_user_top_tracks
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import re
from difflib import SequenceMatcher

load_dotenv()  # Load environment variables from .env
client = OpenAI()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read playlist-modify-public playlist-modify-private user-read-private"
))

def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    return cleaned_string.strip()

def prompt_llm(user_prompt, top_tracks):
    track_descriptions = [f"{t['name']} by {t['artist']}" for t in top_tracks]
    context = "\n".join(track_descriptions)

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert DJ and music recommender. You blend vibes with user history."
            },
            {
                "role": "user",
                "content": f"""
User prompt: "{user_prompt}"

The user often listens to:
{context}

Generate a setlist of 10-20 songs that match the user's taste and fit the described vibe.
Return the setlist as a JSON array of objects with keys 'song' and 'artist'. Only return the json.
"""
            }
        ]
    )

    content = res.choices[0].message.content

    try:
        data = clean_json_string(content)
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Response is not a list")
        for item in data:
            if not all(key in item for key in ("song", "artist")):
                raise ValueError("Missing keys in response item")
        numbered = [
            {"tracknum": i + 1, "song": t["song"], "artist": t["artist"]}
            for i, t in enumerate(data)
        ]
        return numbered
    except Exception as e:
        raise ValueError(f"LLM returned invalid format: {content}") from e


def _similarity(a: str, b: str) -> float:
    """Return a similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _find_best_track(song: str, artist: str, threshold: float = 0.6):
    """Search Spotify for the best matching track.

    The search first looks for both track and artist. Up to five results are
    evaluated using a simple string similarity score. The highest scoring track
    above ``threshold`` is returned. ``None`` is returned if no suitable match
    is found.
    """
    query = f"track:{song} artist:{artist}"
    results = sp.search(q=query, type="track", limit=5)
    target = f"{song} {artist}"
    best = None
    best_score = threshold

    for item in results.get("tracks", {}).get("items", []):
        candidate = f"{item['name']} {item['artists'][0]['name']}"
        score = _similarity(candidate, target)
        if score > best_score:
            best = item
            best_score = score

    return best


def get_spotify_tracks(recommendations, threshold: float = 0.6):
    """Resolve LLM recommendations to Spotify track objects.

    Parameters
    ----------
    recommendations: list[dict]
        Each item must contain ``"song"`` and ``"artist"`` keys.
    threshold: float
        Minimum similarity score required to accept a search result.

    Returns
    -------
    list
        Spotify track objects for all successfully resolved recommendations.
        Entries with no acceptable match are skipped.
    """

    tracks = []
    for rec in recommendations:
        best = _find_best_track(rec["song"], rec["artist"], threshold=threshold)
        if best:
            tracks.append(best)
    return tracks


if __name__ == "__main__":
    user_prompt = input("🎧 What's your vibe? → ")
    top_tracks = get_user_top_tracks()
    try:
        setlist = prompt_llm(user_prompt, top_tracks)
        setlist_spotify = get_spotify_tracks(setlist)
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print("\n🎶 Your Personalized Set:\n")
        i = 0
        for track in setlist_spotify:
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            print(f"{i}. {artist_name} - {track_name}")
            i+=1

