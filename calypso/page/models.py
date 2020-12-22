from django.db import models
from django_grapesjs.models import GrapesJsHtmlField

class Page(models.Model):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    html = GrapesJsHtmlField()
    published= models.BooleanField(default=True)
    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.title

