from django.db import models


class SentEmail(models.Model):
    TEMPLATE_IN_STOCK = 'in-stock'
    TEMPLATE_CHOICES = (
        (TEMPLATE_IN_STOCK, 'In Stock'),
    )

    email = models.EmailField()

    template_name = models.CharField(
        max_length=128,
        choices=TEMPLATE_CHOICES,
    )

    sent_date = models.DateTimeField(
        auto_now_add=True,
    )

    email_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    data = models.TextField(
        null=True,
    )

    class Meta:
        ordering = ('-sent_date',)
