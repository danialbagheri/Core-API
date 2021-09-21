from django.db import models
from django.utils.translation import gettext as _


class Keyword(models.Model):
    """
    keywords to be used for tagging products with different keywords more suitable for search
    example: paraben-free, sensitive lotion , atti-bac, spf20, etc
    """

    name = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name=_('name'),
    )

    def __str__(self):
        return self.name
