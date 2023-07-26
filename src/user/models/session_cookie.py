from django.db import models

from user.models import User


class SessionCookie(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='session_cookies',
    )

    cookie = models.UUIDField()

    expire_date = models.DateTimeField()
