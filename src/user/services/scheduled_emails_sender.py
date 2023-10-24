from django.utils import timezone

from common.services import BaseService
from user.models import ScheduledEmail, SentEmail
from user.services import SubscribeInvitationMailjetEmail, SubscriptionVerifier, EmailOrderVerifier, \
    WelcomeDiscountReminderEmail, CategoriesIntroEmail
from web.models import Configuration


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
                not SubscriptionVerifier(email).is_subscribed()
            ):
                SubscribeInvitationMailjetEmail([email]).send_emails()
            if (
                template == ScheduledEmail.TEMPLATE_WELCOME_DISCOUNT_REMINDER and
                not SentEmail.objects.filter(
                    email=email,
                    template_name=SentEmail.TEMPLATE_WELCOME_DISCOUNT_REMINDER,
                ).exists() and
                not EmailOrderVerifier(email).verify_email_order()
            ):
                discount_code = Configuration.objects.filter(key='welcome-discount-code').first()
                if discount_code:
                    WelcomeDiscountReminderEmail(discount_code.value, [email]).send_emails()
                if not SentEmail.objects.filter(
                    email=email,
                    template_name=SentEmail.TEMPLATE_CATEGORIES_INTRO,
                ).exists():
                    CategoriesIntroEmail([email]).send_emails()
            scheduled_email.email_sent = True
            scheduled_email.save()
