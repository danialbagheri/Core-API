from django.db import models
from product.models import Tag, ProductType, Product
from django.dispatch import receiver
# Create your models here.
from datetime import date
import os


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    excerpt = models.TextField(help_text="A short version of the blog post")
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(ProductType, blank=True)
    # alt_text = models.TextField(blank=True)
    related_products = models.ManyToManyField(Product)

    image = models.ImageField(
        upload_to='static/blog_images', blank=True)
    published = models.BooleanField(default=False, null=True)
    publish_date = models.DateField(
        default=date.today, blank=True, null=True, )

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=BlogPost)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=BlogPost)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = BlogPost.objects.get(pk=instance.pk).image
    except BlogPost.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
