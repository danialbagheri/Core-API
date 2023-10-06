from typing import Any, Dict

from common.services import TransactionalMailJetEmailService
from user.models import SentEmail


class WelcomeDiscountReminderEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_WELCOME_DISCOUNT_REMINDER
    template_config_key = 'welcome-discount-reminder-template-id'

    def __init__(self, discount_code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discount_code = discount_code

    def _get_variables(self) -> Dict[str, Any]:
        return {
            'discount_code': self.discount_code,
        }
