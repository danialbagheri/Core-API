from django.db import models


class SearchQuery(models.Model):
    text = models.CharField(
        max_length=256,
        unique=True,
    )

    count = models.PositiveIntegerField(
        default=0,
    )
