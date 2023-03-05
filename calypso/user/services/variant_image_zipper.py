import io
import zipfile

from product.models import ProductVariant
from user.models import VariantImageRequest
from .image_convertor import ImageConvertor


class VariantImageZipper:
    def __init__(self, sku_list, variant_image_request):
        self.sku_list = sku_list
        self.image_type = variant_image_request.image_type
        self.image_angle = variant_image_request.image_angle
        self.image_format = variant_image_request.image_format
        self.image_convertor = ImageConvertor(self.image_format)
        self.invalid_sku_list = []
        self.sku_list_without_images = []

    def _get_sku_converted_image(self, sku):
        sku = sku.upper()
        variant = ProductVariant.objects.filter(sku=sku).first()
        if not variant:
            self.invalid_sku_list.append(sku)
            return
        variant_image = variant.variant_images
        if self.image_type != VariantImageRequest.TYPE_ALL:
            variant_image = variant_image.filter(image_type=self.image_type)
        if self.image_angle != VariantImageRequest.ANGLE_ALL:
            variant_image = variant_image.filter(image_angle=self.image_angle)
        variant_image = variant_image.first()
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
