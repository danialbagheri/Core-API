import csv
import io
from typing import List

from bs4 import BeautifulSoup

from common.services import BaseService
from product.models import ProductVariant, VariantIngredientThrough


class ImageRequestVariantsCsvBuilder(BaseService):
    def __init__(self, variants_sku_list: List[str]):
        super().__init__(variants_sku_list=variants_sku_list)
        self.variants_sku_list = variants_sku_list

    @staticmethod
    def get_variant_ingredients(variant: ProductVariant):
        variant_ingredients = VariantIngredientThrough.objects.filter(
            variant=variant,
        ).select_related('ingredient').order_by('priority')
        ingredient_names = [variant_ingredient.ingredient.name for variant_ingredient in variant_ingredients]
        ingredient_names_str = ', '.join(ingredient_names)
        ingredient_names_str += '\n\n'
        ingredient_names_str += ('The ingredients listed correspond to the current state of production. '
                                 'Since we regularly adjust our formulations to incorporate new scientific findings, '
                                 'the declaration of ingredients specified on the package applies in each case.')
        return ingredient_names_str

    def build_csv_file(self):
        csv_file = io.StringIO()
        variants = ProductVariant.objects.filter(sku__in=self.variants_sku_list)

        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['SKU', 'Description', 'Ingredients'])
        for variant in variants:
            ingredients = self.get_variant_ingredients(variant)
            description = BeautifulSoup(variant.product.description, features='html.parser').text
            csv_writer.writerow([variant.sku, description, ingredients])
        return csv_file
