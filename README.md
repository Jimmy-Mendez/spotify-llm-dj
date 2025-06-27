# Spotify LLM DJ

This small project generates a custom playlist using your Spotify listening history and an OpenAI model. When you run the script you will be asked to describe the vibe you are looking for. The app then pulls your top tracks from Spotify and asks the OpenAI API to create a numbered setlist of songs that match that vibe.

## Setup

1. **Python packages**

   Install the required packages with pip:

   ```bash
   pip install openai spotipy python-dotenv
   ```

2. **Create a `.env` file**

   Refer to the [Spotify API documentation](https://developer.spotify.com/documentation/web-api) to get required credentials.

   Refer to the [OpenAI documentation](https://openai.com/api/) to get the required credential.

   Both the Spotify and OpenAI clients read their credentials from environment variables. Create a `.env` file in the repository root containing the following values:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   SPOTIPY_CLIENT_ID=your-spotify-client-id
   SPOTIPY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

   The redirect URI must match the one configured for your Spotify application. When running for the first time, Spotipy will open a browser window so you can authorise the app. The OAuth token is cached in `.cache`. 

## Running

A FastAPI server is provided in `api.py` to expose REST
endpoints for creating playlists. Install `fastapi` and `uvicorn` and
run:

```bash
uvicorn api:app
```

Key endpoints:

- `GET /login` – obtain the Spotify authorisation URL.
- `GET /callback` – OAuth redirect URI.
- `POST /playlist` – generate and save the playlist to your account.
- `GET /profile` – return the authenticated user's profile.

A very small web frontend is provided under `static/`. When the API server is
running you can open `http://localhost:8000/` to interact with it:

1. Click **Login with Spotify** to authenticate.
2. Enter your vibe and press **Create Playlist** to generate and save the
   playlist. A link to the playlist will be shown on success.

