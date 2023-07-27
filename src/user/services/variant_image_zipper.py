import io
import zipfile
from typing import Dict, Set

from product.models import ProductImage
from .image_convertor import ImageConvertor


class VariantImageZipper:
    def __init__(self, variant_images: Dict[str, Set[ProductImage]], image_formats):
        self.variant_images = variant_images
        self.image_formats = image_formats
        self.image_convertor = ImageConvertor(self.image_formats)

    def add_sku_images_to_zip(self, zip_file, sku, images):
        count = 0
        for image in images:
            count += 1
            image_type = image.get_image_type_display()
            image_angle = image.get_image_angle_display()
            image_path = image.image.url
            converted_images = self.image_convertor.convert_image(image_path)
            for image_format, image_bytes in converted_images.items():
                zip_file.writestr(f'{sku}/{sku}-{image_type}-{image_angle}-{count}.{image_format}', image_bytes.read())

    def create_zip_file(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for sku, images in self.variant_images.items():
                self.add_sku_images_to_zip(zip_file, sku, images)
        zip_buffer.seek(0)
        return zip_buffer
