from product.models import ProductVariant


class VariantPriceRepresentative:
    @staticmethod
    def _get_variant_ml_number(variant: ProductVariant):
        def extract_number(number_str):
            number = ""
            number_started = False
            for c in number_str:
                if c.isdigit():
                    number += c
                    number_started = True
                elif number_started:
                    return int(number)
            return int(number)

        if not variant.size:
            return None

        litre_const = 1
        quantity_number = 1
        ml_string = variant.size.lower()
        if 'x' in ml_string.lower():
            index = ml_string.index('x')
            quantity_number = ml_string[:index]
            quantity_number = extract_number(quantity_number)
            ml_string = ml_string[index:]

        if 'litre' in ml_string or ('ml' not in ml_string and 'l' in ml_string):
            litre_const = 1000
        ml_number = extract_number(ml_string)

        return ml_number * quantity_number * litre_const

    @staticmethod
    def get_price(variant: ProductVariant):
        return '%.2f' % variant.price

    @staticmethod
    def get_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.compare_at_price if variant.compare_at_price else None

    def get_price_per_100ml(self, variant: ProductVariant):
        ml_number = self._get_variant_ml_number(variant)
        if not ml_number:
            return None
        return '%.2f' % (100 * (variant.price / ml_number))

    @staticmethod
    def get_euro_price(variant: ProductVariant):
        return '%.2f' % variant.euro_price if variant.euro_price else None

    @staticmethod
    def get_euro_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.euro_compare_at_price if variant.euro_compare_at_price else None

    def get_euro_price_per_100ml(self, variant: ProductVariant):
        ml_number = self._get_variant_ml_number(variant)
        if not ml_number or not variant.euro_price:
            return None
        return '%.2f' % (100 * (variant.euro_price / ml_number))
