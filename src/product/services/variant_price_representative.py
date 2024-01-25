from product.models import ProductVariant


class VariantPriceRepresentative:
    def __init__(self, variant: ProductVariant):
        self.variant = variant
        self.ml_number = self._get_variant_ml_number()

    def _get_variant_ml_number(self):
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

        if not self.variant.size:
            return None

        litre_const = 1
        quantity_number = 1
        ml_string = self.variant.size.lower()
        if 'x' in ml_string.lower():
            index = ml_string.index('x')
            quantity_number = ml_string[:index]
            quantity_number = extract_number(quantity_number)
            ml_string = ml_string[index:]

        if 'litre' in ml_string or ('ml' not in ml_string and 'l' in ml_string):
            litre_const = 1000
        ml_number = extract_number(ml_string)

        return ml_number * quantity_number * litre_const

    def get_price(self):
        return '%.2f' % self.variant.price

    def get_compare_at_price(self):
        return '%.2f' % self.variant.compare_at_price if self.variant.compare_at_price else None

    def get_price_per_100ml(self):
        if not self.ml_number:
            return None
        return '%.2f' % (100 * (self.variant.price / self.ml_number))

    def get_euro_price(self):
        return '%.2f' % self.variant.euro_price if self.variant.euro_price else None

    def get_euro_compare_at_price(self):
        return '%.2f' % self.variant.euro_compare_at_price if self.variant.euro_compare_at_price else None

    def get_euro_price_per_100ml(self):
        if not self.ml_number or not self.variant.euro_price:
            return None
        return '%.2f' % (100 * (self.variant.euro_price / self.ml_number))
