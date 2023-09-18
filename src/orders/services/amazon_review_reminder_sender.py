from django.utils import timezone
from sp_api.api import Solicitations

from common.services import BaseService
from user.models import AmazonReviewReminder


class AmazonReviewReminderSender(BaseService):
    service_name = 'Amazon Review Reminder Sender'

    @staticmethod
    def send_reminder_emails():
        now = timezone.now()
        review_reminders = AmazonReviewReminder.objects.filter(
            email_sent=False,
            reminder_date__lt=now,
        )
        for review_reminder in review_reminders:
            Solicitations().create_product_review_and_seller_feedback_solicitation(
                review_reminder.amazon_order.amazon_order_id,
            )
            review_reminder.email_sent = True
            review_reminder.save(update_fields=['email_sent'])
