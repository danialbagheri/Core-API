from product.models import ProductImage, Tag
from django.core.files.images import get_image_dimensions


# This for loop populates the width and height for images
all_images = ProductImage.objects.all()
for im in all_images:
    width, height = get_image_dimensions(im.image.file)
    im.width = width
    im.height = height
    im.save()

# This for loop creates a correct slug for all tags
tags = Tag.objects.all()
for tag in tags:
    try:
        slug_instance = tag.name.replace(' ', '-')
        tag.slug = slug_instance
        tag.save()
    except Exception as e:
        print(e)