from django.db import models

# Create your models here.


class Page(models.Model):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.title
