from django.db import models
from django_grapesjs.models import GrapesJsHtmlField

class Page(models.Model):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    html = models.TextField(blank=True)
    meta_description = models.CharField(max_length=250, blank=True, null=True, default="")
    section_1 = models.TextField(blank=True, help_text="This section is not required and only used on custom pages.",default="")
    section_2 = models.TextField(blank=True, help_text="This section is not required and only used on custom pages.",default="")
    section_3 = models.TextField(blank=True, help_text="This section is not required and only used on custom pages.",default="")
    section_4 = models.TextField(blank=True, help_text="This section is not required and only used on custom pages.",default="")
    published= models.BooleanField(default=True)
    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.title

