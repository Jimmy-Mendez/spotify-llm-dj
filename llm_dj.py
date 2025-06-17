from openai import OpenAI
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

    res = client.chat.completions.create(  # <-- update method name
        model="gpt-4o",  # or "gpt-4.0", "gpt-4-turbo" if using chat
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
Output just the list of song names and artists.
"""
            }
        ]
    )
    return res.choices[0].message.content


if __name__ == "__main__":
    user_prompt = input("🎧 What's your vibe? → ")
    top_tracks = get_user_top_tracks()
    setlist = prompt_llm(user_prompt, top_tracks)
    print("\n🎶 Your Personalized Set:\n")
    print(setlist)

