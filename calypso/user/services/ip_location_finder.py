import requests
from django.conf import settings


class IPLocationFinderService:
    def __init__(self, ip):
        self.ip = ip
        self.country = None

    def receive_location_data(self):
        token = settings.IP_INFO_TOKEN
        url = f'https://ipinfo.io/{self.ip}?token={token}'
        response = requests.get(url)
        if not response.ok:
            return
        self.country = response.json()['country']
