from hackohio.secrets import get_secret

import requests

def get_playlist_tracks(playlist_id):
    url = "https://api-v2.soundcloud.com/playlists/%s" % playlist_id

    secret = get_secret("soundcloud", "client_id")

    params = {
       "representation": "full",
       "client_id": secret,
       "app_version": 1479467323,
   }

    res = requests.get(url, params)

    return res.json()

def get_stream_url(track_id):
    url = "https://api.soundcloud.com/i1/tracks/%s/streams" % track_id

    secret = get_secret("soundcloud", "client_id")

    params = {
       "client_id": secret,
       "app_version": 1479467323,
   }

    res = requests.get(url, params)

    return res.json()

