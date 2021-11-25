from django.db import models


class ContactForm(models.Model):
    REASON_CHOICES = (
        ('Urgent: Change Order detail or Address', 'Urgent: Change Order detail or Address'),
        ('Question about order or Delivery', 'Question about order or Delivery'),
        ('Press Contact & Media', 'Press Contact & Media'),
        ('Wholesale, Discount, promo code query', 'Wholesale, Discount, promo code query'),
        ('Product Question', 'Product Question'),
        ('Other', 'Other'),
    )

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
        choices=REASON_CHOICES,
    )

    message = models.TextField(
        blank=True
    )

    email_sent = models.BooleanField(
        default=False,
    )
