from django.db import models


class Reply(models.Model):
    """
    This models keeps all the replies to the reviews.
    """
    user_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="Linco Care",
    )

    user_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        default="",
    )

    comment = models.TextField()
