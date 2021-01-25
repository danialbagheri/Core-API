from django.conf import settings
import requests

# To gain long lived instant token, I have registered with https://www.instant-tokens.com/
instance_token_api_url = settings.INSTAGRAM_INSTANT_TOKEN_API


def get_instagram_token():
    r = requests.get(instance_token_api_url)
    token = r.json()['Token']
    return token


def get_user_feed():
    access_token = get_instagram_token()
    instagram_user_id = settings.INSTAGRAM_USER_ID
    instagram_media_feed_url = f"https://graph.instagram.com/{instagram_user_id}/media?fields=media_url,caption,permalink,media_type&access_token={access_token}"
    r = requests.get(instagram_media_feed_url)
    response = r.json()['data']
    return response
