from django.db import models


class ContactForm(models.Model):
    email = models.EmailField(
        max_length=256,
    )

    name = models.CharField(
        max_length=256,
        blank=True,
    )

    address = models.CharField(
        max_length=256,
        blank=True,
    )

    subject = models.CharField(
        max_length=256,
        blank=True,
    )

    reason = models.CharField(
        max_length=256,
    )

    message = models.TextField(
        blank=True,
    )

    subscribe_sender = models.BooleanField(
        default=False,
    )

    email_sent = models.BooleanField(
        default=False,
    )

    sent_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    receivers_email = models.CharField(
        max_length=512,
        blank=True,
    )
