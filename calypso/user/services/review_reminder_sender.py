from typing import Optional, List

from django.conf import settings
from django.utils import timezone
from mailchimp_transactional import Client
from mailchimp_transactional.api_client import ApiClientError

from user.models import ReviewReminder
from .review_email_content_builder import ReviewEmailContentBuilder


class ReviewReminderSender:
    def __init__(self):
        self.mailchimp = Client(settings.MAILCHIMP_TRANSACTIONAL_API_KEY)
        self.review_reminders: Optional[List[ReviewReminder]] = None

    def _set_reminders_to_send(self):
        now = timezone.now()
        self.review_reminders = ReviewReminder.objects.filter(
            email_sent=False,
            reminder_date__lt=now,
        )

    def send_reminder_emails(self):
        self._set_reminders_to_send()
        for review_reminder in self.review_reminders:
            variants = list(review_reminder.bought_variants.filter(is_public=True))
            template_content = ReviewEmailContentBuilder(variants).build_content()
            data = {
                'template_name': 'review',
                'template_content': [{'name': 'products', 'content': template_content}],
                'message': {
                    'subject': 'test subject',
                    'To': [{'email': review_reminder.email}],
                },
            }
            try:
                self.mailchimp.messages.send_template(data)
                review_reminder.email_sent = True
                review_reminder.save(update_fields=['email_sent'])
            except ApiClientError:
                pass
