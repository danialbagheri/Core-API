from django.db import models

from user.models import User


class PushSubscriber(models.Model):
    endpoint = models.URLField(
        max_length=1024,
    )

    p256dh = models.TextField()

    auth = models.TextField()

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
