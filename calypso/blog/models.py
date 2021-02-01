from django.db import models
from product.models import Tag, ProductType, Product
from django.dispatch import receiver
# Create your models here.
from datetime import date
import os


class BlogPost(models.Model):

    def blog_image_path(self, filename):
        return f"public/blog_images/{filename}"

    title = models.CharField(max_length=250)
    slug = models.SlugField()
    excerpt = models.TextField(help_text="A short version of the blog post")
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(ProductType, blank=True)
    image_alt_text = models.CharField(max_length=300,blank=True)
    related_products = models.ManyToManyField(Product)

    image = models.ImageField(
        upload_to=blog_image_path, blank=True)
    published = models.BooleanField(default=False, null=True)
    publish_date = models.DateField(
        default=date.today, blank=True, null=True, )

    def __str__(self):
        return self.title


    
