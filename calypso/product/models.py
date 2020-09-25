from django.db import models
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from base64 import b64encode
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from product.shopify import get_variant_info_by_restVariantId, get_variant_info_by_sku
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


class Tag(models.Model):
    '''
    Product tags to be used for tagging products with different keywords
    example: paraben-free, sensitive lotion etc
    '''

    def icons_directory_path(self, filename):
        # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
        return "tags-icon/{0}".format(filename)

    icon = models.ImageField(
        upload_to=icons_directory_path, blank=True)
    name = models.CharField(_('name'), max_length=200, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(_('name'), max_length=300)
    sub_title = models.CharField(_('sub title'), max_length=300)
    slug = models.SlugField(_("slug"), unique=True)
    description = models.TextField(blank=True, null=True)
    direction_of_use = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", verbose_name=_("tags"), blank=True)
    types = models.ManyToManyField(
        "ProductType", verbose_name=_("types"), blank=True)

    @property
    def all_images(self):
        return ProductImage.objects.filter(product__product_category=self)

    @property
    def main_image_object(self):
        return self.all_images.first()

    @property
    def lowest_variant_price(self):
        list_of_prices = []
        for product in self.products.all():
            list_of_prices.append(product.price)
        lowest_price = min(float(sub) for sub in list_of_prices)
        return lowest_price

    @property
    def main_image(self):
        # return self.main_image_object.image.get_absolute_image_url
        return self.all_images.first().get_absolute_image_url

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    '''
    This model holds all product images
    '''

    def image_directory_path(self, filename):
        extension = os.path.splitext(filename)[1]
        random_id = random.randint(100, 120)
        new_file_name = "{}-{}-{}-{}-type-{}-{}-id{}{}".format(
            self.product.product_code, self.product.product_category.name, self.product.option_name, self.product.option_value, self.image_type, self.image_angle, random_id, extension).replace(" ", "_")
        # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
        return "product-images/{0}/{1}/{2}".format(self.product.product_category.name, self.product.product_code, new_file_name).replace(" ", "_")

    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_directory_path)
    image_type = models.CharField(max_length=2, choices=IMAGE_TYPE, blank=True)
    image_angle = models.CharField(
        max_length=10, choices=IMAGE_ANGLE, blank=True)
    alternate_text = models.CharField(max_length=250)

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
    def image_base64(self):
        img = open(self.image.path, "rb")
        data = img.read()
        return str(b64encode(data).decode('utf-8'))

    def __str__(self):
        return "{} - {}".format(self.product.product_category.name, self.product)


class Product(models.Model):

    product_code = models.CharField(max_length=100, blank=True)
    product_category = models.ForeignKey(
        "ProductCategory", null=True, on_delete=models.CASCADE, related_name="products")
    option_name = models.CharField(max_length=255, null=True, blank=True)
    option_value = models.CharField(max_length=200, null=True, blank=True)
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
    # rrp = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, default=0)
    # sale_price = models.FloatField(blank=True, null=True)

    @property
    def image_list(self):
        image_list = []
        for image in self.image:
            image_list.append(image.image_type)
        return image_list

    @property
    def category_product_types(self):
        product_types = []
        for product_type in self.product_category.product_types.all():
            product_types.append(str(product_type))
        return product_types

    @property
    def category_product_tags(self):
        tags = []
        for tag in self.product_category.tags.all():
            tags.append(str(tag))
        return ','.join(tags)

    @property
    def shopify_information(self):
        shopify_info = get_variant_info_by_restVariantId(
            self.shopify_variant_id)
        return [shopify_info]

    @property
    def synchronise_with_shopify(self):
        if self.product_code:
            try:
                info = get_variant_info_by_sku(self.product_code)
                self.price = info['price']
                self.shopify_rest_variant_id = info['legacyResourceId']
                self.shopify_storefront_variant_id = info['storefrontId']
                self.save()
                return True
            except:
                return False

    @property
    def ingredient_list(self):
        pass

    def __str__(self):
        return "{}, {}, {}, {}".format(self.product_code, self.product_category, self.option_name, self.option_value, self.size)


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
    product = models.ForeignKey(
        "Product", null=True, on_delete=models.CASCADE, related_name='wheretobuy')
    stockist = models.ForeignKey(
        "Stockist", null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=250, null=True, blank=True)
