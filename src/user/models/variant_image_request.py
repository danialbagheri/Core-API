from django.db import models


class VariantImageRequest(models.Model):
    TYPE_PRODUCT_IMAGE = 'PI'
    TYPE_LIFE_STYLE = 'LS'
    TYPE_RANGE_PHOTO = 'RP'
    TYPE_TEXTURE = 'TX'
    TYPE_ANIMATION = 'AN'
    TYPE_STUDIO = 'ST'
    TYPE_RESULT = 'RS'
    TYPE_OTHERS = 'OT'
    TYPE_ALL = 'ALL'
    IMAGE_TYPE_CHOICES = (
        (TYPE_PRODUCT_IMAGE, 'Product Image'),
        (TYPE_LIFE_STYLE, 'Life Style'),
        (TYPE_RANGE_PHOTO, 'Range Photo'),
        (TYPE_TEXTURE, 'Texture'),
        (TYPE_ANIMATION, 'Animation'),
        (TYPE_STUDIO, 'Studio'),
        (TYPE_RESULT, 'Result'),
        (TYPE_OTHERS, 'Others'),
        (TYPE_ALL, 'All'),
    )

    ANGLE_FRONT = 'FRONT'
    ANGLE_BACK = 'BACK'
    ANGLE_ANGLE = 'ANGLE'
    ANGLE_TOP = 'TOP'
    ANGLE_RIGHT_SIDE = 'RIGHT-SIDE'
    ANGLE_LEFT_SIDE = 'LEFT-SIDE'
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

    image_types = models.TextField()

    image_angles = models.TextField()

    image_formats = models.TextField()

    no_directories = models.BooleanField(
        default=False,
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
