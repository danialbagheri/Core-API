import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from ipware import get_client_ip
from rest_framework.request import Request

from common.services import BaseService


class RecaptchaValidator(BaseService):
    service_name = 'Recaptcha Validator'

    def __init__(self, recaptcha_value: str):
        super().__init__()
        self.recaptcha_value = recaptcha_value

    def validate(self, request: Request):
        ip, _ = get_client_ip(request)
        response = requests.post(
            url=f'https://www.google.com/recaptcha/api/siteverify?'
                f'secret={settings.DRF_RECAPTCHA_SECRET_KEY}&response={self.recaptcha_value}&remoteip={ip}',
        )
        data = response.json()
        if response.status_code != 200 or not data.get('success', False):
            raise ValidationError('Recaptcha validation failed.')
