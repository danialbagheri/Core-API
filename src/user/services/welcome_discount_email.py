from datetime import timedelta
from typing import Any, Dict

from django.utils import timezone

from common.services import TransactionalMailJetEmailService
from user.models import SentEmail, ScheduledEmail


class WelcomeDiscountEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_WELCOME_DISCOUNT
    template_config_key = 'welcome-discount-template-id'

    def __init__(self, discount_code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discount_code = discount_code

    def _get_variables(self) -> Dict[str, Any]:
        return {
            'discount_code': self.discount_code,
        }

    def send_emails(self) -> None:
        super().send_emails()
        ScheduledEmail.objects.get_or_create(
            recipient_email=self.emails[0],
            template_name=ScheduledEmail.TEMPLATE_WELCOME_DISCOUNT_REMINDER,
            defaults={
                'send_time': timezone.now() + timedelta(days=2),
            },
        )
