from product.models import ProductImage
from django.core.files.images import get_image_dimensions


all_images = ProductImage.objects.all()
for im in all_images:
    width, height = get_image_dimensions(im.image.file)
    im.width = width
    im.height = height
    im.save()