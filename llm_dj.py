from openai import OpenAI
import json
import spotipy
from user_data import get_user_top_tracks
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
client = OpenAI()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-private"))

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

Generate a setlist of 10 songs that match the user's taste and fit the described vibe.
Return the setlist as a JSON array of objects with keys 'song' and 'artist'.
"""
            }
        ]
    )

    content = res.choices[0].message.content

    try:
        data = json.loads(content)
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


if __name__ == "__main__":
    user_prompt = input("🎧 What's your vibe? → ")
    top_tracks = get_user_top_tracks()
    try:
        setlist = prompt_llm(user_prompt, top_tracks)
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print("\n🎶 Your Personalized Set:\n")
        for track in setlist:
            print(f"{track['tracknum']}. {track['song']} - {track['artist']}")

