from django.db import models

from product.models import ProductVariant


class InstagramPost(models.Model):
    MEDIA_TYPE_IMAGE = 'IMAGE'
    MEDIA_TYPE_VIDEO = 'VIDEO'
    MEDIA_TYPE_ALBUM = 'CAROUSEL_ALBUM'
    MEDIA_TYPE_CHOICES = (
        (MEDIA_TYPE_IMAGE, 'Image'),
        (MEDIA_TYPE_VIDEO, 'Video'),
        (MEDIA_TYPE_ALBUM, 'Album'),
    )

    instagram_id = models.CharField(
        max_length=64,
    )

    media_type = models.CharField(
        max_length=64,
    )

    media_url = models.URLField(
        max_length=512,
    )

    thumbnail = models.URLField(
        max_length=512,
    )

    webp = models.URLField(
        max_length=512,
    )

    caption = models.TextField(
        blank=True,
    )

    permalink = models.CharField(
        max_length=512,
        blank=True,
    )

    variants = models.ManyToManyField(
        to=ProductVariant,
        through='web.VariantInstagramRelation',
        related_name='instagram_posts',
    )


class VariantInstagramRelation(models.Model):
    instagram_post = models.ForeignKey(
        to=InstagramPost,
        on_delete=models.CASCADE,
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
    )
