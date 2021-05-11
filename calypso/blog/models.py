from django.db import models
from product.models import Tag, ProductType, Product
from django.utils.html import strip_tags
from django.core.files.images import get_image_dimensions
# Create your models here.
from datetime import date


class BlogPost(models.Model):

    def blog_image_path(self, filename):
        return f"public/blog_images/{filename}"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300)
    excerpt = models.TextField(help_text="A short version of the blog post", blank=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(ProductType, blank=True)
    image_alt_text = models.CharField(max_length=300,blank=True)
    related_products = models.ManyToManyField(Product, blank=True)
    image_width = models.IntegerField(blank=True)
    image_height = models.IntegerField(blank=True)
    image = models.ImageField(
        upload_to=blog_image_path, blank=True, height_field='image_height', width_field='image_width')
    published = models.BooleanField(default=False, null=True)
    publish_date = models.DateField(
        default=date.today, blank=True, null=True, )

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        a = strip_tags(self.body)
        return len(a.split())

    @property
    def read_time(self):
        time = int(self.word_count / 200)
        if time == 0:
            time += 1
        return "{} min read.".format(time)

    def save(self, *args, **kwargs):
        if self.image:
            width, height = get_image_dimensions(self.image.open().file, close=True)
            self.image_width = width
            self.image_height = height
        else:
            self.image_width = 0
            self.image_height = 0

        super(BlogPost, self).save(*args, **kwargs)