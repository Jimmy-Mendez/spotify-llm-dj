from openai import OpenAI
import json
import spotipy
from user_data import get_user_top_tracks
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import re

load_dotenv()  # Load environment variables from .env
client = OpenAI()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-private"))

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

