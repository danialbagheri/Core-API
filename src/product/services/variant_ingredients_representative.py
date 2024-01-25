from common.services import BaseService
from product.models import VariantIngredientThrough


class VariantIngredientsRepresentative(BaseService):
    def __init__(self, variant):
        super().__init__(variant=variant)
        self.variant = variant

    def get_ingredients(self):
        if not VariantIngredientThrough.objects.exists():
            return list(self.variant.ingredients.all().values_list('name', flat=True))
        variant_ingredients = VariantIngredientThrough.objects.filter(
            variant=self.variant,
        ).select_related('ingredient').order_by('priority')
        ingredient_names = [variant_ingredient.ingredient.name for variant_ingredient in variant_ingredients]
        return ingredient_names
