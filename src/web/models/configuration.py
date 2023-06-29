from django.db import models
from django.utils.text import slugify


class Configuration(models.Model):
    """
    A key and Value database of different settings and models.
    Fixtures needs to be applied at the initial setup.
    """

    name = models.CharField(
        max_length=250,
        unique=True,
    )

    key = models.CharField(
        max_length=250,
        unique=True,
    )

    value = models.CharField(
        max_length=350,
    )

    active = models.BooleanField(
        default=True,
    )

    description = models.CharField(
        max_length=250,
        default='',
        blank=True,
        null=True,
    )

    setting = models.ManyToManyField(
        to='web.Setting',
        blank=True,
        related_name='configuations',
    )

    def save(self, *args, **kwargs):
        self.key = slugify(self.key, allow_unicode=True)
        super(Configuration, self).save(*args, **kwargs)

    def __str__(self):
        return "{} = {}".format(self.key, self.value)
