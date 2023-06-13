from typing import Optional, List

from django.utils import timezone

from user.models import ReviewReminder
from . import ReviewReminderMailjetEmail


class ReviewReminderSender:
    def __init__(self):
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
            email = review_reminder.email
            ReviewReminderMailjetEmail(variants, [email]).send_emails()
            review_reminder.email_sent = True
            review_reminder.save(update_fields=['email_sent'])
