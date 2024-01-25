from django.db import models

from bundles.models import Bundle


class BundleImage(models.Model):
    IMAGE_TYPE_PRODUCT_IMAGE = 'PI'
    IMAGE_TYPE_LIFE_STYLE = 'LS'
    IMAGE_TYPE_RANGE_PHOTO = 'RP'
    IMAGE_TYPE_TEXTURE = 'TX'
    IMAGE_TYPE_ANIMATION = 'AN'
    IMAGE_TYPE_STUDIO = 'ST'
    IMAGE_TYPE_RESULT = 'RS'
    IMAGE_TYPE_OTHERS = 'OT'
    IMAGE_TYPE_CHOICES = (
        (IMAGE_TYPE_PRODUCT_IMAGE, 'Product Image'),
        (IMAGE_TYPE_LIFE_STYLE, 'Life Style'),
        (IMAGE_TYPE_RANGE_PHOTO, 'Range Photo'),
        (IMAGE_TYPE_TEXTURE, 'Texture'),
        (IMAGE_TYPE_ANIMATION, 'Animation'),
        (IMAGE_TYPE_STUDIO, 'Studio'),
        (IMAGE_TYPE_RESULT, 'Result'),
        (IMAGE_TYPE_OTHERS, 'Others'),
    )

    IMAGE_ANGLE_FRONT = 'FRONT'
    IMAGE_ANGLE_BACK = 'BACK'
    IMAGE_ANGLE_ANGLE = 'ANGLE'
    IMAGE_ANGLE_TOP = 'TOP'
    IMAGE_ANGLE_RIGHT_SIDE = 'RIGHT-SIDE'
    IMAGE_ANGLE_LEFT_SIDE = 'LEFT-SIDE'
    IMAGE_ANGLE_BOTTOM = 'BOTTOM'
    IMAGE_ANGLE_CUSTOM = 'CUSTOM'
    IMAGE_ANGLE_CHOICES = (
        (IMAGE_ANGLE_FRONT, 'Front'),
        (IMAGE_ANGLE_BACK, 'Back'),
        (IMAGE_ANGLE_ANGLE, 'Angle'),
        (IMAGE_ANGLE_TOP, 'Top'),
        (IMAGE_ANGLE_RIGHT_SIDE, 'Right Side'),
        (IMAGE_ANGLE_LEFT_SIDE, 'Left Side'),
        (IMAGE_ANGLE_BOTTOM, 'Bottom'),
        (IMAGE_ANGLE_CUSTOM, 'Custom'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    bundle = models.ForeignKey(
        to=Bundle,
        on_delete=models.CASCADE,
        related_name='images',
    )

    image = models.ImageField(
        upload_to='bundles/',
    )

    alternate_text = models.CharField(
        max_length=256,
        blank=True,
    )

    image_type = models.CharField(
        max_length=2,
        choices=IMAGE_TYPE_CHOICES,
    )

    image_angle = models.CharField(
        max_length=16,
        choices=IMAGE_ANGLE_CHOICES,
    )

    main = models.BooleanField(
        default=False,
    )

    position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return "{} - {} - {}".format(
            self.bundle.name,
            self.get_image_type_display(),
            self.get_image_angle_display()
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.main:
            self.bundle.images.exclude(id=self.id).update(main=False)
