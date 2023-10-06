from django.db import models

from user.models import SentEmail


class ScheduledEmail(models.Model):
    TEMPLATE_REVIEW_REMINDER = SentEmail.TEMPLATE_REVIEW_REMINDER
    TEMPLATE_SUBSCRIBE_INVITATION = SentEmail.TEMPLATE_SUBSCRIBE_INVITATION
    TEMPLATE_WELCOME_DISCOUNT_REMINDER = SentEmail.TEMPLATE_WELCOME_DISCOUNT_REMINDER
    TEMPLATE_CHOICES = (
        (TEMPLATE_REVIEW_REMINDER, 'Review Reminder'),
        (TEMPLATE_SUBSCRIBE_INVITATION, 'Subscribe Invitation'),
        (TEMPLATE_WELCOME_DISCOUNT_REMINDER, 'Welcome Discount Reminder')
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    recipient_email = models.EmailField()

    template_name = models.CharField(
        max_length=128,
        choices=TEMPLATE_CHOICES,
    )

    send_time = models.DateTimeField(
        db_index=True,
    )

    email_sent = models.BooleanField(
        default=False,
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
    )
