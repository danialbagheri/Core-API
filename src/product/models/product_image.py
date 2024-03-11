import os
import random
from base64 import b64encode

import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.images import get_image_dimensions
from django.db import models
from django.utils.safestring import mark_safe

from product.models import ProductVariant


class ProductImage(models.Model):
    """
    This model holds all product images
    """
    IMAGE_TYPE = (
        ('PI', 'Product Image'),
        ('LS', 'Life Style'),
        ('RP', 'Range Photo'),
        ('TX', 'Texture'),
        ('AN', 'Animation'),
        ('ST', 'Studio'),
        ('RS', 'Result'),
        ('OT', 'Others'),
    )

    IMAGE_ANGLE = (
        ('FRONT', 'Front'),
        ('BACK', 'Back'),
        ('ANGLE', 'Angle'),
        ('TOP', 'Top'),
        ('RIGHT-SIDE', 'Right Side'),
        ('LEFT-SIDE', 'Left Side'),
        ('BOTTOM', 'Bottom'),
        ('CUSTOM', 'Custom'),
    )

    def image_directory_path(self, filename):
        extension = os.path.splitext(filename)[1]
        random_id = random.randint(100, 120)
        new_file_name = "{}-{}-{}-type-{}-{}-id{}{}".format(
            self.variant.sku, self.variant.product.name, self.variant.name,
            self.image_type, self.image_angle, random_id, extension
        ).replace(" ", "_")
        # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
        return "product-images/{0}/{1}/{2}".format(
            self.variant.product.name, self.variant.sku, new_file_name
        ).replace(" ", "_")

    name = models.CharField(
        max_length=128,
        blank=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
        related_name='variant_images',
    )

    image = models.ImageField(
        upload_to=image_directory_path,
        height_field='height',
        width_field='width',
    )

    image_type = models.CharField(
        max_length=2,
        choices=IMAGE_TYPE,
        blank=True,
    )

    image_angle = models.CharField(
        max_length=10,
        choices=IMAGE_ANGLE,
        blank=True,
    )

    alternate_text = models.CharField(
        max_length=250,
    )

    height = models.IntegerField(
        blank=True,
    )

    width = models.IntegerField(
        blank=True,
    )

    main = models.BooleanField(
        default=False,
    )

    is_public = models.BooleanField(
        default=True,
    )

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" />'.format(self.image.url))
        return mark_safe('<p style="background-color:#c2c2c2;padding: 5px 10px;"> Please upload an image. </p>')

    image_preview.short_description = 'Image'
    image_preview.allow_tags = True

    @property
    def get_absolute_image_url(self):
        # url = Site.objects.first()
        request = None
        return "{0}{1}".format(get_current_site(request).domain, self.image.url)

    @property
    def get_(self):
        # url = Site.objects.first()
        request = None
        return "{0}{1}".format(get_current_site(request).domain, self.image.url)

    @property
    def image_base64(self):
        response = requests.get(self.image.url)
        data = response.content
        return str(b64encode(data).decode('utf-8'))

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.variant.product.name, self.variant)

    def save(self, *args, **kwargs):
        self.width = 0
        self.height = 0
        if self.image:
            width, height = get_image_dimensions(
                self.image.open().file, close=False
            )
            self.width = width
            self.height = height

        if self.main:
            try:
                ProductImage.objects.filter(
                    variant=self.variant
                ).exclude(pk=self.pk).update(main=False)
            except:
                pass
        super(ProductImage, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-image_type']
