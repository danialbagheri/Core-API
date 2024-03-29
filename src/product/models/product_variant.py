from django.db import models
from django.utils.translation import gettext as _

from product.models import Product, Ingredient
from product.shopify import get_variant_info_by_restVariantId, get_variant_info_by_sku


class ProductVariant(models.Model):

    sku = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
    )

    ASIN = models.CharField(
        max_length=64,
        blank=True,
    )

    product = models.ForeignKey(
        to=Product,
        null=True,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="",
    )

    shopify_rest_variant_id = models.CharField(
        max_length=355,
        unique=True,
    )

    graphql_id = models.CharField(
        max_length=512,
        unique=True,
    )

    shopify_storefront_variant_id = models.CharField(
        max_length=355,
        blank=True,
        null=True,
    )

    barcode = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    date_first_available = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    date_last_modified = models.DateField(
        auto_now=True,
        null=True,
        blank=True,
    )

    claims = models.TextField(
        blank=True,
        null=True,
    )

    ingredients = models.ManyToManyField(
        to=Ingredient,
        blank=True,
        verbose_name=_('ingredients'),
    )

    discontinued = models.BooleanField(
        default=False,
    )

    size = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    rrp = models.FloatField(
        blank=True,
        null=True,
    )

    price = models.FloatField(
        blank=True,
        null=True,
        default=0,
    )

    compare_at_price = models.FloatField(
        blank=True,
        null=True,
    )

    euro_price = models.FloatField(
        blank=True,
        null=True,
    )

    euro_compare_at_price = models.FloatField(
        blank=True,
        null=True,
    )

    inventory_quantity = models.IntegerField(
        blank=True,
        null=True,
    )

    is_public = models.BooleanField(
        default=False,
    )

    position = models.IntegerField(
        null=True,
        blank=True,
    )

    @property
    def image_list(self):
        image_list = []
        for image in self.variant_images:
            image_list.append(image.image_type)
        return image_list

    @property
    def category_product_types(self):
        product_types = []
        for product_type in self.product.product_types.all():
            product_types.append(str(product_type))
        return product_types

    @property
    def category_product_tags(self):
        tags = []
        for tag in self.product.tags.all():
            tags.append(str(tag))
        return ','.join(tags)

    @property
    def shopify_information(self):
        shopify_info = get_variant_info_by_restVariantId(
            self.shopify_variant_id
        )
        return [shopify_info]

    @property
    def synchronise_with_shopify(self):
        if not self.sku:
            return False
        try:
            info = get_variant_info_by_sku(self.sku)
            self.price = info['price']
            self.compare_at_price = info['compareAtPrice']
            self.shopify_rest_variant_id = info['legacyResourceId']
            self.shopify_storefront_variant_id = info['storefrontId']
            self.inventory_quantity = info['inventoryQuantity']
            self.barcode = info['barcode']
            self.position = info['position']
            presentment_prices = info['presentmentPrices']['edges']
            if not presentment_prices:
                self.save()
                return True
            euro_info = presentment_prices[0]['node']
            self.euro_price = euro_info['price']['amount']
            if euro_info['compareAtPrice']:
                self.euro_compare_at_price = euro_info['compareAtPrice']['amount']
            self.save()
            return True
        except:
            return False

    @property
    def ingredient_list(self):
        pass

    def __str__(self):
        return '{}, {}, {}'.format(self.sku, self.product, self.name, self.size)

    def save(self, *args, **kwargs):
        old_object = None
        if self.pk:
            old_object = ProductVariant.objects.get(pk=self.pk)
        super().save(*args, **kwargs)
        if self.inventory_quantity == 0 and old_object.inventory_quantity > 0:
            self.out_of_stock = True
