import hashlib
import hmac
import logging
import time
from typing import List, Tuple

import requests
from django.conf import settings

from common.services import BaseService
from web.models import Configuration

logger = logging.getLogger(__name__)


class TiktokClient(BaseService):
    service_name = 'TikTok Client'

    def __init__(self):
        super().__init__()
        self.app_key = settings.TIKTOK_APP_KEY
        self.app_secret = settings.TIKTOK_APP_SECRET

    def _get_tiktok_request_signature(self, path, params: List[Tuple[str, str]]):
        signature_string = f'{self.app_secret}{path}'
        for param in params:
            signature_string += f'{param[0]}{param[1]}'
        signature_string += self.app_secret
        signature = hmac.new(self.app_secret.encode(), signature_string.encode(), hashlib.sha256).hexdigest()
        return signature

    def send_get_request(self, path, params):
        params['app_key'] = self.app_key
        params['timestamp'] = int(time.time())
        sorted_params = [(key, params[key]) for key in sorted(params.keys())]
        request_signature = self._get_tiktok_request_signature(path, sorted_params)
        params['access_token'] = settings.TIKTOK_ACCESS_TOKEN
        params['sign'] = request_signature
        url = f'{settings.TIKTOK_API_URL}{path}'
        response = requests.get(url, params=params)
        return response.json()

    def send_post_request(self, path, body):
        params = {
            'app_key': self.app_key,
            'timestamp': int(time.time())
        }
        sorted_params = [(key, params[key]) for key in sorted(params.keys())]
        request_signature = self._get_tiktok_request_signature(path, sorted_params)
        params['access_token'] = settings.TIKTOK_ACCESS_TOKEN
        params['sign'] = request_signature
        url = f'{settings.TIKTOK_API_URL}{path}'
        response = requests.post(url, json=body, params=params)
        return response.json()

    def refresh_access_token(self):
        refresh_token_config = Configuration.objects.filter(key='tiktok_refresh_token').first()
        if not refresh_token_config:
            logger.exception(msg='TikTok refresh token not found in configuration')
            return

        url = f'{settings.TIKTOK_AUTH_URL}/api/v2/token/refresh'
        params = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'refresh_token': refresh_token_config.value,
            'grant_type': 'refresh_token',
        }
        response = requests.get(url, params=params)
        data = response.json()['data']
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        Configuration.objects.filter(key='tiktok_refresh_token').update(value=refresh_token)
        Configuration.objects.update_or_create(
            key='tiktok_access_token',
            defaults={'value': access_token},
        )
