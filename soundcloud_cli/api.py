import requests
from soundcloud_cli.config import get_config_value

BASE_URL="https://api-v2.soundcloud.com"

class SoundCloudClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            })
        client_id = get_config_value("client_id")
        self.session.params = {"client_id": client_id}

    def search(self, query, limit=10):
        if not query:
            raise ValueError("Query not given")

        response = self.session.get(BASE_URL+"/search/tracks", params={"q":query, "limit" : limit})

        response.raise_for_status()

        response_object = response.json()
        tracks = [{"id":track["id"],
                   "title":track["title"],
                   "duration":track["duration"],
                   "permalink_url":track["permalink_url"],
                   "username":track["user"]["username"],
                   "transcodings":track["media"]["transcodings"],
                   "playback_count":track.get("playback_count",0),
                   "artwork_url": track.get("artwork_url", None)
                   } for track in response_object["collection"]]
        return tracks

    def get_stream_url(self, transcodings):
        if not transcodings:
            raise ValueError("No transcodings provided")
        progressive = next((t for t in transcodings if t["format"]["protocol"] == "progressive"), None)
        if not progressive:
            raise ValueError("No progressive stream available for the track!")

        streamable_url = self.session.get(progressive["url"])
        return streamable_url.json()["url"]


