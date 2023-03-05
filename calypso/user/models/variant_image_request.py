from django.db import models


class VariantImageRequest(models.Model):
    TYPE_PRODUCT_IMAGE = 'PI'
    TYPE_LIFE_STYLE = 'LS'
    TYPE_RANGE_PHOTO = 'RP'
    TYPE_OTHERS = 'OT'
    TYPE_ALL = 'ALL'
    IMAGE_TYPE_CHOICES = (
        (TYPE_PRODUCT_IMAGE, 'Product Image'),
        (TYPE_LIFE_STYLE, 'Life Style'),
        (TYPE_RANGE_PHOTO, 'Range Photo'),
        (TYPE_OTHERS, 'Others'),
        (TYPE_ALL, 'All'),
    )

    ANGLE_FRONT = 'FRONT'
    ANGLE_BACK = 'BACK'
    ANGLE_ANGLE = 'ANGLE'
    ANGLE_TOP = 'TOP'
    ANGLE_RIGHT_SIDE = 'RIGHT_SIDE'
    ANGLE_LEFT_SIDE = 'LEFT_SIDE'
    ANGLE_BOTTOM = 'BOTTOM'
    ANGLE_CUSTOM = 'CUSTOM'
    ANGLE_ALL = 'ALL'
    IMAGE_ANGLE_CHOICES = (
        (ANGLE_FRONT, 'Front'),
        (ANGLE_BACK, 'Back'),
        (ANGLE_ANGLE, 'Angle'),
        (ANGLE_TOP, 'Top'),
        (ANGLE_RIGHT_SIDE, 'Right Side'),
        (ANGLE_LEFT_SIDE, 'Left Side'),
        (ANGLE_BOTTOM, 'Bottom'),
        (ANGLE_CUSTOM, 'Custom'),
        (ANGLE_ALL, 'ALL'),
    )

    created = models.DateTimeField(auto_now_add=True)

    sku_list = models.TextField()

    image_type = models.CharField(
        max_length=32,
        default=TYPE_ALL,
        choices=IMAGE_TYPE_CHOICES,
    )

    image_angle = models.CharField(
        max_length=32,
        default=ANGLE_ALL,
        choices=IMAGE_ANGLE_CHOICES,
    )

    image_format = models.CharField(
        max_length=16,
    )

    email = models.EmailField()

    zip_file = models.FileField(
        max_length=512,
        upload_to='variant-image-zips/',
        blank=True,
        null=True,
    )

    email_sent = models.BooleanField(
        default=False,
    )
