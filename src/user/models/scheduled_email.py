from django.contrib.postgres.fields import JSONField
from django.db import models

from user.models import SentEmail


class ScheduledEmail(models.Model):
    TEMPLATE_REVIEW_REMINDER = SentEmail.TEMPLATE_REVIEW_REMINDER
    TEMPLATE_SUBSCRIBE_INVITATION = SentEmail.TEMPLATE_SUBSCRIBE_INVITATION
    TEMPLATE_CHOICES = (
        (TEMPLATE_REVIEW_REMINDER, 'Review Reminder'),
        (TEMPLATE_SUBSCRIBE_INVITATION, 'Subscribe Invitation'),
    )

    recipient_email = models.EmailField()

    template_name = models.CharField(
        max_length=128,
        choices=TEMPLATE_CHOICES,
    )

    send_time = models.DateTimeField()

    extra_data = JSONField(
        null=True,
        blank=True,
    )
