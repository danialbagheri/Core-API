import ast
from collections import defaultdict
from typing import Dict, Set

from product.models import ProductImage
from user.models import VariantImageRequest


class VariantImagesRetriever:
    def __init__(self, variant_image_request: VariantImageRequest):
        self.sku_list = ast.literal_eval(variant_image_request.sku_list)
        self.sku_list = [sku.upper() for sku in self.sku_list]
        self.image_types = ast.literal_eval(variant_image_request.image_types)
        self.image_angles = ast.literal_eval(variant_image_request.image_angles)
        self.variant_images: Dict[str, Set[ProductImage]] = defaultdict(set)
        self.sku_list_without_image = set(self.sku_list)

    def retrieve_variant_image(self):
        images = ProductImage.objects.filter(variant__sku__in=self.sku_list).select_related('variant')
        if VariantImageRequest.TYPE_ALL not in self.image_types:
            images = images.filter(image_type__in=self.image_types)
        if VariantImageRequest.ANGLE_ALL not in self.image_angles:
            images = images.filter(image_angle__in=self.image_angles)

        for image in images:
            sku = image.variant.sku
            self.variant_images[sku].add(image)
            self.sku_list_without_image.discard(sku)
