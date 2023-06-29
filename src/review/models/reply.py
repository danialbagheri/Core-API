from django.db import models


class Reply(models.Model):
    """
    This models keeps all the replies to the reviews.
    """
    user_name = models.CharField(
        max_length=200,
    )

    user_email = models.EmailField(
        max_length=254,
    )

    comment = models.TextField()
