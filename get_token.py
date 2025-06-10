import requests

def load_credentials(filepath="creds.txt"):
    creds = {}
    with open(filepath, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                creds[key.strip()] = value.strip()
    return creds["CLIENT_ID"], creds["CLIENT_SECRET"]

def get_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.status_code} - {response.text}")
    return response.json()["access_token"]

def store_token(token, filepath="token.txt"):
    with open(filepath, "w") as f:
        f.write(token)

if __name__ == "__main__":
    cid, secret = load_credentials("creds.txt")
    token = get_access_token(cid, secret)
    store_token(token)
    print("✅ Access token stored in token.txt")

