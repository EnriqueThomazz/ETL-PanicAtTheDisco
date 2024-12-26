import requests as rq
import json

from dotenv import load_dotenv
import os

artist_id = "20JZFwl6HVl6yg8a4H3ZqK"

# Getting the access token
load_dotenv("./credentials.env")

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

# with spotify API, you need to post your credentials in order to receive a time-limited access token
response = rq.post("https://accounts.spotify.com/api/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                      data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret})

res = json.loads(response.text)

access_token = res["access_token"]

# Getting the albums from the artist and saving them
response = rq.get(f"https://api.spotify.com/v1/artists/{artist_id}/albums",
                  headers={"Authorization": f"Bearer {access_token}"})

albums = json.loads(response.text)["items"]

with open("./Raw/albums.json", "w") as output:
    json.dump(albums, output)


# Getting the tracks from every album
tracks = []

for item in albums:
    response = rq.get(f"https://api.spotify.com/v1/albums/{item["id"]}/tracks",
                    headers={"Authorization": f"Bearer {access_token}"})
    
    tracks += json.loads(response.text)["items"]

with open("./Raw/tracks.json", "w") as output:
    json.dump(tracks, output)