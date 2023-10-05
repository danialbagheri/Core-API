import logging

from celery import Task, current_app

from user.services import WelcomeDiscountEmail
from web.models import Configuration

logger = logging.getLogger(__name__)


class SendWelcomeDiscountEmailTask(Task):
    name = 'user.tasks.SendWelcomeDiscountEmailTask'

    def run(self, email):
        discount_code = Configuration.objects.filter(key='welcome-discount-code').first()
        if not discount_code:
            logger.exception('Welcome discount code not created yet.')
            return
        WelcomeDiscountEmail(discount_code, [email]).send_emails()


current_app.register_task(SendWelcomeDiscountEmailTask())
