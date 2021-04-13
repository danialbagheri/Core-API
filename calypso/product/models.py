from django.db import models
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from base64 import b64encode
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from product.shopify import get_variant_info_by_restVariantId, get_variant_info_by_sku
# from django.dispatch import receiver
import os
import random
# Create your models here.
# for translation use this format:
#     name = models.CharField(_('name'), help_text=_('This is the help text'))
IMAGE_TYPE = (
    ('PI', 'Product Image'),
    ('LS', 'Life Style'),
    ('RP', 'Range Photo'),
    ('OT', 'Others'),
)
IMAGE_ANGLE = (
    ('FRONT', 'Front'),
    ('BACK', 'Back'),
    ('ANGLE', 'Angle'),
    ('TOP', 'Top'),
    ('RIGHT-SIDE', 'Right Side'),
    ('LEFT-SIDE', 'Left Side'),
    ('BOTTOM', 'Bottom'),
    ('CUSTOM', 'Custom'),
)

IMAGE_FORMAT = (
    ('PNG', 'Transparent PNG'),
    ('JPEG', 'Original JPEG'),
    ('TIFF', 'High Quality TIFF'),
    ('GIF', 'Animation GIF'),
)


class ProductType(models.Model):
    '''
    Product types example:
    sun protection, after sun, skin care etc.
    '''
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return self.name

def get_slug():
    import random
    
    slug_instance = random.randint(22,9991)
    return slug_instance

class Tag(models.Model):
    '''
    Tags to be used for tagging products with different benefits
    example: paraben-free, sensitive lotion etc
    '''

    def icons_directory_path(self, filename):
        # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
        return "tags-icon/{0}".format(filename)

    icon = models.ImageField(
        upload_to=icons_directory_path, blank=True)
    name = models.CharField(_('name'), max_length=200, blank=True)
    slug = models.SlugField(_("slug"), unique=True, default=get_slug())

    # def get_slug(self):
    #     slug_instance = self.name.replace(' ', '-')
    #     return slug_instance

    def __str__(self):
        return self.name

class Keyword(models.Model):
    '''
    keywords to be used for tagging products with different keywords more suitable for search
    example: paraben-free, sensitive lotion , atti-bac, spf20, etc
    '''

    name = models.CharField(_('name'), max_length=200, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('name'), max_length=300)
    sub_title = models.CharField(_('sub title'), max_length=300)
    slug = models.SlugField(_("slug"), unique=True)
    description = models.TextField(blank=True, null=True)
    direction_of_use = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", verbose_name=_("tags"), blank=True)
    keyword = models.ManyToManyField("Keyword", verbose_name=_("keywords"), blank=True)
    types = models.ManyToManyField(
        "ProductType", verbose_name=_("types"), blank=True)
    top_seller = models.BooleanField(default=False)

    @property
    def all_images(self):
        return ProductImage.objects.filter(variant__product=self)

    @property
    def main_image_object(self):
        return self.all_images.first()

    @property
    def lowest_variant_price(self):
        list_of_prices = []
        for variant in self.variants.all():
            list_of_prices.append(variant.price)
        try:
            lowest_price = min(float(sub) for sub in list_of_prices)
        except:
            lowest_price = None
        return lowest_price

    @property
    def main_image(self):
        # return self.main_image_object.image.get_absolute_image_url
        try:
            main_image = self.all_images.first().get_absolute_image_url
        except:
            main_image = None
        return main_image

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    '''
    This model holds all product images
    '''

    def image_directory_path(self, filename):
        extension = os.path.splitext(filename)[1]
        random_id = random.randint(100, 120)
        new_file_name = "{}-{}-{}-type-{}-{}-id{}{}".format(
            self.variant.sku, self.variant.product.name, self.variant.name, self.image_type, self.image_angle, random_id, extension).replace(" ", "_")
        # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
        return "product-images/{0}/{1}/{2}".format(self.variant.product.name, self.variant.sku, new_file_name).replace(" ", "_")

    variant = models.ForeignKey(
        'ProductVariant', on_delete=models.CASCADE, related_name='variant_images')
    image = models.ImageField(upload_to=image_directory_path, height_field='height', width_field='width')
    image_type = models.CharField(max_length=2, choices=IMAGE_TYPE, blank=True)
    image_angle = models.CharField(
        max_length=10, choices=IMAGE_ANGLE, blank=True)
    alternate_text = models.CharField(max_length=250)
    height = models.IntegerField()
    width = models.IntegerField()

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" />'.format(self.image.url))
        else:
            return mark_safe('<p style="background-color:#c2c2c2;padding: 5px 10px;"> Please upload an image. </p>')

    image_preview.short_description = 'Image'
    image_preview.allow_tags = True

    @property
    def get_absolute_image_url(self):
        # url = Site.objects.first()
        request = None
        return "{0}{1}".format(get_current_site(request).domain, self.image.url)
    @property
    def get_(self):
        # url = Site.objects.first()
        request = None
        return "{0}{1}".format(get_current_site(request).domain, self.image.url)

    @property
    def image_base64(self):
        img = open(self.image.path, "rb")
        data = img.read()
        return str(b64encode(data).decode('utf-8'))

    def __str__(self):
        return "{} - {}".format(self.variant.product.name, self.variant)


class ProductVariant(models.Model):

    sku = models.CharField(max_length=100, blank=True, unique=True)
    product = models.ForeignKey(
        "Product", null=True, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=255, null=True, blank=True, default="")
    size = models.CharField(max_length=355, blank=True)
    shopify_rest_variant_id = models.CharField(
        max_length=355, blank=True, null=True)
    shopify_storefront_variant_id = models.CharField(
        max_length=355, blank=True, null=True)
    date_first_available = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    date_last_modified = models.DateField(
        auto_now=True, null=True, blank=True)
    claims = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        "Ingredient", verbose_name=_("ingredients"))
    discontinued = models.BooleanField(default=False)
    size = models.CharField(max_length=200, null=True, blank=True)
    rrp = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, default=0)
    inventory_quantity = models.IntegerField(blank=True, null=True)
    # sale_price = models.FloatField(blank=True, null=True)

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
            self.shopify_variant_id)
        return [shopify_info]

    @property
    def synchronise_with_shopify(self):
        if self.sku:
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


class Ingredient(models.Model):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return self.name


class Stockist(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(
        upload_to="where-to-buy/logos", null=True, blank=True)

    def __str__(self):
        return self.name


class WhereToBuy(models.Model):
    variant = models.ForeignKey(
        "ProductVariant", null=True, on_delete=models.CASCADE, related_name='wheretobuy')
    stockist = models.ForeignKey(
        "Stockist", null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=250, null=True, blank=True)


class Collection(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    products = models.ManyToManyField(
        'Product',
        blank=True,
        related_name="collections",
    )

    background_image_alt = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# @receiver(models.signals.post_delete, sender=ProductImage)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)


# @receiver(models.signals.pre_save, sender=ProductImage)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#     try:
#         old_file = ProductImage.objects.get(pk=instance.pk).image
#     except ProductImage.DoesNotExist:
#         return False

#     new_file = instance.image
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
