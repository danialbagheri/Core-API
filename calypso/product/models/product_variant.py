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
        blank=True,
        null=True,
    )

    shopify_storefront_variant_id = models.CharField(
        max_length=355,
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
        verbose_name=_("ingredients"),
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

    inventory_quantity = models.IntegerField(
        blank=True,
        null=True,
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
            self.shopify_rest_variant_id = info['legacyResourceId']
            self.shopify_storefront_variant_id = info['storefrontId']
            self.inventory_quantity = info['inventoryQuantity']
            self.save()
            return True
        except:
            return False

    @property
    def ingredient_list(self):
        pass

    def __str__(self):
        return "{}, {}, {}".format(self.sku, self.product, self.name, self.size)
