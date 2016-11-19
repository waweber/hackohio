import re
import tweepy
import requests
import json
from hackohio.secrets import get_secret

MICROSOFT_API_BASE = 'https://westus.api.cognitive.microsoft.com/'
TEXT_ANALYSIS_URL = MICROSOFT_API_BASE + 'text/analytics/v2.0/sentiment'

class Mood:

    # Returns a mood from 0 to 1, where 0 is bad and 1 is good
    @classmethod
    def _mood_from_text(cls, text):
        headers = {
            'Ocp-Apim-Subscription-Key': get_secret('microsoft_text', 'key_1')
        }

        body = {"documents": [ {"language": "en", "id": "0", "text": text} ] }
        r = requests.post(TEXT_ANALYSIS_URL, headers=headers, data=json.dumps(body))

        response_json = r.json()
        return response_json['documents'][0]["score"]

    # Gets the mood for the most recent tweet by a user
    @classmethod
    def mood_from_twitter(cls, handle):
        key = get_secret('twitter', 'consumer_key')
        secret = get_secret('twitter', 'consumer_secret')
        auth = tweepy.OAuthHandler(key, secret)

        print(key)
        print(secret)
        print(auth)
        api = tweepy.API(auth)

        most_recent_tweet = api.user_timeline(screen_name=handle, count=1)[0]
        tweet_text = most_recent_tweet.text

        # Strip out @'s and hashtags for purity
        clean = re.sub(r'@\w+\s*', '', tweet_text)
        clean = re.sub(r'#', '', clean)

        mood = cls._mood_from_text(clean)

        if (mood > 0.65):
            return 'happy'
        elif (mood < 0.45):
            return'sad'

        return 'neutral'
