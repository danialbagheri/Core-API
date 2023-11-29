from django.conf import settings
from mailjet_rest import Client

from common.services import BaseService
from web.models import Configuration


class SubscriptionVerifier(BaseService):
    service_name = 'Subscription Verifier'
    MAILJET_LIST_ID_CONFIG_KEY = 'main-contact-list-id'

    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3',
        )
        self.main_list_id = None
        list_id_config = Configuration.objects.filter(key=self.MAILJET_LIST_ID_CONFIG_KEY).first()
        if list_id_config:
            self.main_list_id = list_id_config.value

    def is_subscribed(self):
        response = self.mailjet.contact_getcontactslists.get(id=self.email)
        if not response.ok:
            return False
        lists = response.json()['Data']
        list_ids = {contact_list['ListID'] for contact_list in lists if not contact_list['IsUnsub']}
        return self.main_list_id in list_ids
