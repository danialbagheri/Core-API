from blog.models import BlogPost
from django.core.files.images import get_image_dimensions


blogs = BlogPost.objects.all()
for im in blogs:
    if im.image:
        width, height = get_image_dimensions(im.image.open().file, close=True)
        im.image_width = width
        im.image_height = height
        im.save()