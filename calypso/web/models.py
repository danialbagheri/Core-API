from django.db import models

# Create your models here.


class Slider(models.Model):
    name = models.CharField("name", max_length=150)
    slug = models.SlugField()
    slides = models.ManyToManyField("web.Slide", verbose_name="slides")
    mobile = models.BooleanField()

    def __str__(self):
        return self.name


class Slide(models.Model):
    name = models.CharField("name", max_length=150)
    order = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=None)
    active = models.BooleanField(default=False)
    custom_slide = models.BooleanField(default=False)
    custom_code = models.TextField()
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
