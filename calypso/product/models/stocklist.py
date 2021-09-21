from django.db import models


class Stockist(models.Model):
    name = models.CharField(
        max_length=250,
    )

    logo = models.ImageField(
        upload_to="where-to-buy/logos",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
