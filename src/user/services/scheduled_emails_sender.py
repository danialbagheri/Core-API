from django.utils import timezone

from common.services import BaseService
from user.models import ScheduledEmail
from user.services import SubscribeInvitationMailjetEmail


class ScheduledEmailsSender(BaseService):
    service_name = 'Scheduled Email Sender'

    @staticmethod
    def send_scheduled_emails():
        emails_to_send = ScheduledEmail.objects.filter(
            send_time__lt=timezone.now(),
            email_sent=False,
        )
        for scheduled_email in emails_to_send:
            template = scheduled_email.template_name
            if template == ScheduledEmail.TEMPLATE_SUBSCRIBE_INVITATION:
                SubscribeInvitationMailjetEmail([scheduled_email.recipient_email]).send_emails()
            scheduled_email.email_sent = True
            scheduled_email.save()
