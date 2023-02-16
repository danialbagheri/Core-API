from django.db import models


class VariantImageRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    sku_list = models.TextField()

    zip_file = models.FileField(
        max_length=512,
        upload_to='variant-image-zips/',
        blank=True,
        null=True,
    )

    email = models.EmailField()
