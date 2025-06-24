# Spotify LLM DJ

This small project generates a custom playlist using your Spotify listening history and an OpenAI model. When you run the script you will be asked to describe the vibe you are looking for. The app then pulls your top tracks from Spotify and asks the OpenAI API to create a numbered setlist of songs that match that vibe.

## Setup

1. **Python packages**

   Install the required packages with pip:

   ```bash
   pip install openai spotipy python-dotenv
   ```

2. **Create a `.env` file**

   Both the Spotify and OpenAI clients read their credentials from environment variables. Create a `.env` file in the repository root containing the following values:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   SPOTIPY_CLIENT_ID=your-spotify-client-id
   SPOTIPY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

   The redirect URI must match the one configured for your Spotify application. When running for the first time, Spotipy will open a browser window so you can authorise the app. The OAuth token is cached in `.cache`.

## Running

Execute the main script:

```bash
python llm_dj.py
```

You will be prompted for a description of the vibe you want. After authorising with Spotify, the program prints a numbered list of song recommendations. These recommendations are derived from your top tracks combined with the prompt you supplied.

## Files

- `llm_dj.py` – main CLI that prompts the model and prints the setlist.
- `user_data.py` – helper that fetches your top tracks using the Spotify Web API.

Enjoy your personalised DJ set!
