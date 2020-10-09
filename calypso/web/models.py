from django.db import models
from django.utils.text import slugify
# Create your models here.


class Slider(models.Model):
    name = models.CharField("name", max_length=150)
    slug = models.SlugField()
    slides = models.ManyToManyField(
        "web.Slide", verbose_name="slides", blank=True)
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


class Setting(models.Model):
    name = models.CharField("name", max_length=150)
    slug = models.SlugField(default='', editable=False)
    description = models.CharField(
        max_length=350, default="", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Configuration(models.Model):
    '''
    A key and Value database of different settings and models. 
    Fixtures needs to be applied at the initial setup.
    '''
    key = models.CharField(max_length=250, unique=True)
    value = models.CharField(max_length=350)
    description = models.CharField(
        max_length=250, default="", blank=True, null=True)
    setting = models.ManyToManyField(
        "web.Setting", blank=True, related_name="configuations")

    def save(self, *args, **kwargs):
        self.key = slugify(self.key, allow_unicode=True)
        super(Configuration, self).save(*args, **kwargs)

    def __str__(self):
        return "{} = {}".format(self.key, self.value)
