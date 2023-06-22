from django.conf import settings

from common.services import InternalEmailService
from web.models import Configuration


class ManagerEmailService(InternalEmailService):
    def get_variables(self):
        raise NotImplementedError

    def get_from_email(self):
        return settings.SERVER_EMAIL

    def get_recipient_emails(self):
        manager_emails_config = Configuration.objects.get(key='manager-emails').value
        manager_emails = manager_emails_config.split(',')
        return manager_emails

    def get_reply_to_emails(self):
        return None
