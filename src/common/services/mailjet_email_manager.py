import logging
from enum import Enum

from django.conf import settings
from mailjet_rest import Client

from common.services import BaseService
from user.models import User
from web.models import Configuration

logger = logging.getLogger(__name__)


class MailjetEmailStatus(Enum):
    PREVIOUSLY_SUBBED = 'PREVIOUSLY_SUBBED'
    PREVIOUSLY_UNSUBBED = 'PREVIOUSLY_UNSUBBED'
    SUBBED = 'SUBBED'
    UNSUBBED = 'UNSUBBED'
    REMOVED = 'REMOVED'
    NOT_SUBBED = 'NOT_SUBBED'
    UNKNOWN = 'UNKNOWN'


class MailjetEmailManager(BaseService):
    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3',
        )
        self.mailjet_email_status = MailjetEmailStatus.UNKNOWN
        self.contact_list_id = None
        contact_list_id_config = Configuration.objects.filter(key='main-contact-list-id').first()
        if contact_list_id_config:
            self.contact_list_id = contact_list_id_config.value

    def _create_contact(self):
        data = {
            'Email': self.email,
            'IsExcludedFromCampaigns': False,
        }
        self.mailjet.contact.create(data=data)

    def _do_action(self, action):
        if not self.contact_list_id:
            logger.error(msg='Contact list configuration not set.')
            return False
        data = {
            'ContactsLists': [
                {'ListID': self.contact_list_id, 'Action': action},
            ],
        }
        response = self.mailjet.contact_managecontactslists.create(id=self.email, data=data)
        if not response.ok:
            logger.error(f'Failed to subscribe email {self.email}')
            return False
        return True

    def subscribe_email(self):
        self._create_contact()
        is_subscribed = self.validate()
        if is_subscribed:
            self.mailjet_email_status = MailjetEmailStatus.PREVIOUSLY_SUBBED
        if not is_subscribed and self.mailjet_email_status != MailjetEmailStatus.PREVIOUSLY_UNSUBBED:
            is_subscribed = self._do_action('addnoforce')
            self.mailjet_email_status = MailjetEmailStatus.SUBBED
        if is_subscribed:
            User.objects.filter(email=self.email).update(is_subscribed=True)
        return is_subscribed

    def remove_email(self):
        is_removed = self._do_action('remove')
        if is_removed:
            User.objects.filter(email=self.email).update(is_subscribed=False)
            self.mailjet_email_status = MailjetEmailStatus.REMOVED
        return is_removed

    def unsub_email(self):
        is_unsubscribed = self._do_action('unsub')
        if is_unsubscribed:
            User.objects.filter(email=self.email).update(is_subscribed=False)
            self.mailjet_email_status = MailjetEmailStatus.UNSUBBED
        return is_unsubscribed

    def validate(self):
        if not self.contact_list_id:
            logger.error(msg='Contact list configuration not set.')
            return False
        response = self.mailjet.contact_getcontactslists.get(id=self.email)
        if response.status_code != 200:
            return False

        results = response.json()['Data']
        for result in results:
            if result['ListID'] != int(self.contact_list_id):
                continue

            if result['IsUnsub']:
                self.mailjet_email_status = MailjetEmailStatus.PREVIOUSLY_UNSUBBED
                return False
            if result['IsActive']:
                self.mailjet_email_status = MailjetEmailStatus.PREVIOUSLY_SUBBED
                return True
            return False
        self.mailjet_email_status = MailjetEmailStatus.NOT_SUBBED
        return False
