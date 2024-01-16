import logging

from django.conf import settings
from mailjet_rest import Client

from common.services import BaseService
from web.models import Configuration

logger = logging.getLogger(__name__)


class MailjetEmailSubscriber(BaseService):
    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3',
        )

    def subscribe_email(self):
        contact_list_id = Configuration.objects.filter(key='main-contact-list-id').first()
        if not contact_list_id:
            logger.error(msg='Contact list configuration not set.')
            return
        data = {
            'ContactsLists': [
                {'ListID': contact_list_id.value, 'Action': 'addforce'},
            ],
        }
        response = self.mailjet.contact_managecontactslists.create(id=self.email, data=data)
        if not response.ok:
            logger.error(f'Failed to subscribe email {self.email}')
