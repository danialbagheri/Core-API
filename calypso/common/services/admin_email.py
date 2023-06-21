from django.conf import settings

from common.services import InternalEmailService
from web.models import Configuration


class AdminEmailService(InternalEmailService):
    def get_variables(self):
        raise NotImplementedError

    def get_from_email(self):
        return settings.SERVER_EMAIL

    def get_recipient_emails(self):
        admin_emails_config = Configuration.objects.get(key='admin-emails').value
        admin_emails = admin_emails_config.split(',')
        return admin_emails

    def get_reply_to_emails(self):
        return None
