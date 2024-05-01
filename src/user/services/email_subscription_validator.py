from django.conf import settings
from mailjet_rest import Client

from common.services import BaseService
from web.models import Configuration


class EmailSubscriptionValidator(BaseService):
    service_name = 'Email Subscription Validator'

    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3',
        )
        self.main_contact_list_id = Configuration.objects.filter(key='main-contact-list-id').first().value

    def validate(self):
        response = self.mailjet.contact_getcontactslists.get(id=self.email)
        if response.status_code != 200:
            return False

        results = response.json()['Data']
        for result in results:
            if (result['IsActive'] or result['IsUnsub']) and result['ListID'] == self.main_contact_list_id:
                return True
        return False
