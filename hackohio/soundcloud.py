from hackohio.secrets import get_secret
import logging

import requests
import random

logger = logging.getLogger(__name__)

def get_playlist_tracks(playlist_id):
    url = "https://api-v2.soundcloud.com/playlists/%s" % playlist_id

    secret = get_secret("soundcloud", "client_id")

    params = {
        "representation": "full",
        "client_id": secret,
        "app_version": 1479467323,
    }

    res = requests.get(url, params)

    data = res.json()

    tracks = data["tracks"]

    full_tracks = [t for t in tracks if "user" in t]
    partial_tracks = [t for t in tracks if "user" not in t]

    if len(partial_tracks) > 0:
        partial_ids = [str(t["id"]) for t in partial_tracks]

        url = "https://api-v2.soundcloud.com/tracks"

        params = {
            "ids": ",".join(partial_ids),
            "client_id": secret,
            "app_version": 1479467323,
        }

        res = requests.get(url, params)

        data = res.json()

        full_tracks.extend(data)

    random.shuffle(full_tracks);

    return full_tracks

def get_stream_url(track_id):
    url = "https://api.soundcloud.com/i1/tracks/%s/streams" % track_id

    secret = get_secret("soundcloud", "client_id")

    params = {
       "client_id": secret,
       "app_version": 1479467323,
   }

    res = requests.get(url, params)

    return res.json()

def get_data(track_id):
    streams = get_stream_url(track_id)

    url = streams["http_mp3_128_url"]

    res = requests.get(url)
    data = res.content

    return data
