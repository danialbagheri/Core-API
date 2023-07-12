from django.db import models


class TopBar(models.Model):
    name = models.CharField(
        max_length=256,
    )

    is_active = models.BooleanField()

    position = models.IntegerField()
