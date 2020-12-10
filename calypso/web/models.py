from django.db import models
from django.utils.text import slugify
from ordered_model.models import OrderedModel
# Create your models here.


class Slider(models.Model):
    name = models.CharField("name", max_length=150)
    slug = models.SlugField()
    slides = models.ManyToManyField(
        "web.Slide", verbose_name="slides", blank=True, related_name='slider')
    mobile = models.BooleanField()

    def __str__(self):
        return self.name


class Slide(models.Model):
    name = models.CharField("name", max_length=150)
    image = models.ImageField(
        upload_to="slide/", height_field=None, width_field=None, max_length=None, blank=True)
    active = models.BooleanField(default=False)
    custom_slide = models.BooleanField(default=False)
    custom_code = models.TextField(blank=True)
    link = models.URLField(null=True, blank=True)
    # order_with_respect_to = 'slider__slug'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SliderSlidesThroughModel(OrderedModel):
    slider = models.ForeignKey(
        Slider, on_delete=models.CASCADE, related_name="slider_slides")
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    order_with_respect_to = 'slider'

    class Meta:
        ordering = ('slider', 'order')


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
    name = models.CharField(max_length=250, unique=True)
    key = models.CharField(max_length=250, unique=True)
    value = models.CharField(max_length=350)
    active = models.BooleanField(default=True)
    description = models.CharField(
        max_length=250, default="", blank=True, null=True)
    setting = models.ManyToManyField(
        "web.Setting", blank=True, related_name="configuations")

    def save(self, *args, **kwargs):
        self.key = slugify(self.key, allow_unicode=True)
        super(Configuration, self).save(*args, **kwargs)

    def __str__(self):
        return "{} = {}".format(self.key, self.value)
