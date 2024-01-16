from django.conf import settings
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
        solicitations_resource = Solicitations(credentials=settings.AMAZON_SP_API_CREDENTIALS)
        for review_reminder in review_reminders:
            amazon_order_id = review_reminder.amazon_order.amazon_order_id
            possible_actions = solicitations_resource.get_solicitation_actions_for_order(
                amazonOrderId=amazon_order_id,
            )._links['actions']
            if possible_actions:
                solicitations_resource.create_product_review_and_seller_feedback_solicitation(
                    amazonOrderId=amazon_order_id,
                )
            review_reminder.email_sent = True
            review_reminder.save(update_fields=['email_sent'])
