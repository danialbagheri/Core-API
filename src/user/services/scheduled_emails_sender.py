from django.utils import timezone

from common.services import BaseService
from user.models import ScheduledEmail, SentEmail
from user.services import SubscribeInvitationMailjetEmail, EmailSubscriptionValidator


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
            email = scheduled_email.recipient_email
            if (
                template == ScheduledEmail.TEMPLATE_SUBSCRIBE_INVITATION and
                not SentEmail.objects.filter(
                    email=email,
                    template_name=SentEmail.TEMPLATE_SUBSCRIBE_INVITATION,
                ).exists() and
                not EmailSubscriptionValidator(email).validate()
            ):
                SubscribeInvitationMailjetEmail([email]).send_emails()
            scheduled_email.email_sent = True
            scheduled_email.save()
