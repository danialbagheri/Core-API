from common.services import BaseService
from product.models import ProductVariant, Product
from surveys.models import SurveySubmission


class SPFFinderRecommender(BaseService):
    def __init__(self, survey_submission: SurveySubmission):
        super().__init__(email=survey_submission.email)
        answers = survey_submission.answers.all()
        self.chosen_choices = set()
        for answer in answers:
            choices = answer.choices.all()
            self.chosen_choices.update([choice.slug for choice in choices])

    def _get_valid_products(self):
        filters = {'is_public': True}
        excludes = {}
        if 'kids-6' in self.chosen_choices:
            filters['types__slug'] = 'kids'
        elif 'myself' in self.chosen_choices:
            excludes['types__slug'] = 'kids'

        if 'lotion' in self.chosen_choices:
            filters['keywords__name'] = 'lotion'
        elif 'spray' in self.chosen_choices:
            filters['keywords__name'] = 'spray'
        elif 'oil' in self.chosen_choices:
            filters['keywords__name'] = 'oil'
        return set(Product.objects.filter(**filters).exclude(**excludes))

    def _get_valid_variants(self):
        products = self._get_valid_products()
        filters = {'is_public': True, 'name__in': ['SPF 30', 'SPF 40', 'SPF 50', 'SPF 50+']}
        if 'desert-n-africa-dubai' in self.chosen_choices:
            filters['name__in'] = ['SPF 50', 'SPF 50+']
        if 'very-pale-skin' in self.chosen_choices or 'fair-skin' in self.chosen_choices:
            filters['name__in'] = ['SPF 40', 'SPF 50', 'SPF 50+']
        variants = ProductVariant.objects.filter(**filters).select_related('product')
        valid_variants = [variant for variant in variants if variant.product in products]
        if valid_variants:
            return valid_variants
        return variants

    @staticmethod
    def _sort_variants(variants, keyword):
        high_priority_variants = []
        low_priority_variants = []

        for variant in variants:
            product = variant.product
            if product.keyword.filter(name=keyword).exists():
                high_priority_variants.append(variant)
                continue
            low_priority_variants.append(variant)
        return high_priority_variants + low_priority_variants

    def _sort_variants_based_on_attribute(self, variants):
        attribute_name = (
            'once a day' if 'apply-once-only' in self.chosen_choices else
            'sensitive' if 'suitable-for-sensitive-skin' in self.chosen_choices else
            None
        )
        if not attribute_name:
            return variants
        return self._sort_variants(variants, attribute_name)

    def _sort_variants_based_on_application(self, variants):
        attribute_name = (
            'face' if 'face' in self.chosen_choices else
            'hair' if 'hair' in self.chosen_choices else
            None
        )
        if not attribute_name:
            return variants
        return self._sort_variants(variants, attribute_name)

    def get_recommended_variants(self):
        variants = self._get_valid_variants()
        variants = self._sort_variants_based_on_attribute(variants)
        return self._sort_variants_based_on_application(variants)
