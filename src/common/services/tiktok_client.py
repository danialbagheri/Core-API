import hashlib
import hmac
import time
from typing import List, Tuple

import requests
from django.conf import settings

from common.services import BaseService


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
