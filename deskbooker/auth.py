import json

import requests


# Get access token
def get_access_token(token_key, refresh_token):
    url = "https://securetoken.googleapis.com/v1/token"
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(url, params={"key": token_key}, data=data)
    access_token = json.loads(response.text)["access_token"]
    return access_token
