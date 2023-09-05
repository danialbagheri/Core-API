from django.db import models

from common.model_mixins import AutoSlugifyMixin


class Page(AutoSlugifyMixin,
           models.Model):
    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True,
    )

    title = models.CharField(
        max_length=250,
    )
    slug_name_field = 'title'

    created = models.DateTimeField(
        auto_now_add=True,
    )

    html = models.TextField(
        blank=True,
    )

    meta_description = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        default='',
    )

    section_1 = models.TextField(
        blank=True,
        help_text='This section is not required and only used on custom pages.',
        default='',
    )

    section_2 = models.TextField(
        blank=True,
        help_text='This section is not required and only used on custom pages.',
        default='',
    )

    section_3 = models.TextField(
        blank=True,
        help_text='This section is not required and only used on custom pages.',
        default='',
    )

    section_4 = models.TextField(
        blank=True,
        help_text='This section is not required and only used on custom pages.',
        default='',
    )

    published = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.title
