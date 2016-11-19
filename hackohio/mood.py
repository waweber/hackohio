import re
import tweepy
import requests
import json
from hackohio.secrets import get_secret

TEXT_ANALYSIS_URL = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
PICTURE_ANALYSIS_URL = 'https://api.projectoxford.ai/emotion/v1.0/recognize'

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

    @classmethod
    def mood_from_picture(cls, picture):
        headers = {
            'Ocp-Apim-Subscription-Key': get_secret('microsoft_pic', 'key_1'),
            'Content-Type': 'application/octet-stream'
        }


        pic_data = picture.read()
        r = requests.post(PICTURE_ANALYSIS_URL, headers=headers, data=pic_data)
        response_json = r.json()

        # Find strongest emotion
        max_val = 0
        max_emotion = 'neutral'
        for key, value in response_json[0]["scores"].items():
            if value > max_val:
                max_val = value
                max_emotion = key

        # Standardize the emotion
        if max_emotion == 'happiness':
            return 'happy'
        elif max_emotion == 'sadness':
            return 'sad'
        elif max_emotion == 'fear':
            return 'sad'
        elif max_emotion == 'anger':
            return 'angry'
        elif max_emotion == 'disgust':
            return 'angry'
        elif max_emotion == 'contempt':
            return 'angry'

        return 'neutral'
