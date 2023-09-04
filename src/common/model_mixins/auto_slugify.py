from django.utils.text import slugify


class AutoSlugifyMixin:
    slug_name_field = 'name'
    slug = None

    def save(self, *args, **kwargs):
        if not self.slug:
            name = getattr(self, self.slug_name_field)
            self.slug = slugify(name)
        super().save(*args, **kwargs)
