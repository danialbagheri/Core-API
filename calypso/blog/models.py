from django.db import models
from product.models import Tag, ProductType
# Create your models here.


# class BlogPost(models.Model):
#     title = models.CharField(max_length=250)
#     slug = models.SlugField()
#     excerpt = models.TextField()
#     body = models.TextField()
#     cover_image = models.ImageField(upload_to='static/blog_images', blank=True)
#     tags = models.ManyToManyField(Tag, blank=True)
#     category = models.ManyToManyField(ProductType, blank=True)
#     mobile_cover_image = models.ImageField(
#         upload_to='static/blog_images/mobile', blank=True)
#     # alt_text = models.TextField(blank=True)
#     related_products = models.ManyToManyField(ProductCategory)

#     catalogue_image = models.ImageField(
#         upload_to='static/blog_images', blank=True)
