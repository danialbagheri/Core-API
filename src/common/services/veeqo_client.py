import hashlib
import hmac
import time
from typing import List, Tuple

import requests
from django.conf import settings

from common.services import BaseService


class VeeqoClient(BaseService):
    service_name = 'Veeqo Client'

    def __init__(self):
        super().__init__()
        self.api_key = settings.VEEQO_API_KEY
 

    def send_get_request(self, path):
        params = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
        }
        
        url = f'{settings.VEEQO_API_URL}{path}'
        response = requests.get(url, timeout=10)
        return response.json()
