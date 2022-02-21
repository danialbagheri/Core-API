from django.db import models

from web.models import TopBar


class TopBarItem(models.Model):
    top_bar = models.ForeignKey(
        to=TopBar,
        on_delete=models.CASCADE,
        related_name='items',
    )

    text = models.TextField(
        blank=True,
    )

    icon = models.ImageField(
        upload_to='top-bar-icons/',
        max_length=512,
        blank=True,
        null=True,
    )

    url = models.URLField(
        max_length=256,
        blank=True,
    )

    is_active = models.BooleanField()

    position = models.IntegerField()
