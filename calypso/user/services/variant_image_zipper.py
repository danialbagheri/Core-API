import io
import zipfile

from product.models import ProductVariant
from .image_convertor import ImageConvertor


class VariantImageZipper:
    def __init__(self, sku_list, image_format):
        self.sku_list = sku_list
        self.image_format = image_format
        self.image_convertor = ImageConvertor(self.image_format)
        self.invalid_sku_list = []
        self.sku_list_without_images = []

    def _get_sku_converted_image(self, sku):
        sku = sku.upper()
        variant = ProductVariant.objects.filter(sku=sku).first()
        if not variant:
            self.invalid_sku_list.append(sku)
            return
        variant_image = variant.variant_images.first()
        if not variant_image:
            self.sku_list_without_images.append(sku)
            return
        image_path = variant_image.image.path
        return self.image_convertor.convert_image(image_path)

    def create_zip_file(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for sku in self.sku_list:
                converted_image = self._get_sku_converted_image(sku)
                zip_file.writestr(f'{sku}.{self.image_format}', converted_image.read())
        zip_buffer.seek(0)
        return zip_buffer
