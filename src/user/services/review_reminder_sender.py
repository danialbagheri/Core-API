from django.utils import timezone

from user.models import ReviewReminder
from . import ReviewReminderMailjetEmail


class ReviewReminderSender:

    @staticmethod
    def send_reminder_emails():
        now = timezone.now()
        review_reminders = ReviewReminder.objects.filter(
            email_sent=False,
            reminder_date__lt=now,
        )
        for review_reminder in review_reminders:
            variants = list(review_reminder.bought_variants.filter(is_public=True))
            email = review_reminder.email
            ReviewReminderMailjetEmail(variants, [email]).send_emails()
            review_reminder.email_sent = True
            review_reminder.save(update_fields=['email_sent'])
