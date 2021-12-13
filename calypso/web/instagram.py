from datetime import datetime, timedelta

import requests
from django.conf import settings

from web.models import Configuration


def refresh_instagram_access_token(access_token):
    url = f'https://graph.instagram.com/refresh_access_token?' \
          f'grant_type=ig_refresh_token&' \
          f'access_token={access_token}'
    response = requests.get(url)
    new_token = response.json()['access_token']
    Configuration.objects.filter(key='instagram_access_token').update(value=new_token)
    Configuration.objects.filter(
        key='instagram_access_token_timestamp'
    ).update(value=datetime.now().strftime('%Y-%m-%d'))
    return response.json()['access_token']


def get_user_feed():
    token_config = Configuration.objects.filter(key='instagram_access_token').first()
    if not token_config:
        return []
    access_token = token_config.value
    access_token_timestamp = Configuration.objects.filter(key='instagram_access_token_timestamp').first()
    if (
        access_token_timestamp and
        datetime.now() - datetime.strptime(access_token_timestamp.value, '%Y-%m-%d') > timedelta(days=30)
    ):
        access_token = refresh_instagram_access_token(access_token)

    instagram_user_id = settings.INSTAGRAM_USER_ID
    instagram_media_feed_url = f"https://graph.instagram.com/{instagram_user_id}/media?" \
                               f"fields=media_url,caption,permalink,media_type&" \
                               f"access_token={access_token}"
    r = requests.get(instagram_media_feed_url)
    response = r.json()['data']
    return response
