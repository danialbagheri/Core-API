import logging

from django.conf import settings
from mailjet_rest import Client

from common.services import BaseService
from user.models import User
from web.models import Configuration

logger = logging.getLogger(__name__)


class MailjetEmailManager(BaseService):
    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3',
        )

    def _do_action(self, action):
        contact_list_id = Configuration.objects.filter(key='main-contact-list-id').first()
        if not contact_list_id:
            logger.error(msg='Contact list configuration not set.')
            return False
        data = {
            'ContactsLists': [
                {'ListID': contact_list_id.value, 'Action': action},
            ],
        }
        response = self.mailjet.contact_managecontactslists.create(id=self.email, data=data)
        if not response.ok:
            logger.error(f'Failed to subscribe email {self.email}')
            return False
        return True

    def subscribe_email(self):
        success = self._do_action('addnoforce')
        if success:
            User.objects.filter(email=self.email).update(is_subscribed=True)

    def remove_email(self):
        self._do_action('remove')

    def unsub_email(self):
        self._do_action('unsub')
