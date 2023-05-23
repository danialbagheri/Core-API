import ast
from typing import Dict

from django.core.exceptions import ValidationError

from product.models import ProductVariant
from user.models import VariantImageRequest


class ImageRequestFiltersValidator:
    def __init__(self, request_filters: Dict):
        self.request_filters = request_filters
        self.email = request_filters['email']
        self.sku_list = request_filters['sku_list']
        self.image_types = request_filters['image_types']
        self.image_angles = request_filters['image_angles']
        self.image_formats = request_filters['image_formats']

    def validate_email(self):
        if '@lincocare.com' not in self.email:
            raise ValidationError({'email': 'Email must be from the domain "lincocare.com"'})

    def validate_sku_list(self):
        self.sku_list = ast.literal_eval(self.sku_list)
        self.sku_list = [sku.upper() for sku in self.sku_list]
        existing_sku_set = set(ProductVariant.objects.filter(sku__in=self.sku_list).values_list('sku', flat=True))
        invalid_sku_set = set(self.sku_list) - existing_sku_set
        if invalid_sku_set:
            raise ValidationError({'invalid_sku_list': list(invalid_sku_set)})

    def validate_image_types(self):
        self.image_types = ast.literal_eval(self.image_types)
        valid_image_types = {image_type[0] for image_type in VariantImageRequest.IMAGE_TYPE_CHOICES}
        invalid_image_types = set(self.image_types) - valid_image_types
        if invalid_image_types:
            raise ValidationError({'invalid_image_types': list(invalid_image_types)})

    def validate_image_angles(self):
        self.image_angles = ast.literal_eval(self.image_angles)
        self.image_angles = [image_angle.upper() for image_angle in self.image_angles]
        valid_image_angles = {image_angle[0] for image_angle in VariantImageRequest.IMAGE_ANGLE_CHOICES}
        invalid_image_angles = set(self.image_angles) - valid_image_angles
        if invalid_image_angles:
            raise ValidationError({'invalid_image_angles': list(invalid_image_angles)})

    def validate(self):
        self.validate_email()
        self.validate_sku_list()
        self.validate_image_types()
        self.validate_image_angles()
        self.image_formats = ast.literal_eval(self.image_formats)
