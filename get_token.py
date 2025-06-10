import requests

# Read creds.txt
def load_credentials(filepath="creds.txt"):
    creds = {}
    with open(filepath, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                creds[key.strip()] = value.strip()
    return creds["CLIENT_ID"], creds["CLIENT_SECRET"]

# Request access token
def get_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

    token_data = response.json()
    return token_data["access_token"]

# Example usage
if __name__ == "__main__":
    client_id, client_secret = load_credentials("creds.txt")
    access_token = get_access_token(client_id, client_secret)
    print(f"🎫 Access Token:\n{access_token}")

