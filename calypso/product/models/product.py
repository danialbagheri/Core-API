from django.db import models
from django.db.models import Avg, Min
from django.utils.translation import gettext as _

from product.models import Tag, Keyword, ProductType


class Product(models.Model):
    updated = models.DateTimeField(
        auto_now=True,
    )

    name = models.CharField(
        max_length=300,
        verbose_name=_('name'),
    )

    legacy_id = models.BigIntegerField(
        blank=True,
        null=True,
    )

    graphql_id = models.CharField(
        max_length=512,
        blank=True,
        null=True,
    )

    sub_title = models.CharField(
        max_length=300,
        verbose_name=_('sub title'),
    )

    slug = models.SlugField(
        unique=True,
        verbose_name=_("slug"),
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    direction_of_use = models.TextField(
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        verbose_name=_("tags"),
    )

    keyword = models.ManyToManyField(
        to=Keyword,
        blank=True,
        verbose_name=_("keywords"),
    )

    types = models.ManyToManyField(
        to=ProductType,
        verbose_name=_("types"),
        blank=True,
    )

    is_public = models.BooleanField(
        default=False,
    )

    main_image = models.OneToOneField(
        to='product.ProductImage',
        on_delete=models.SET_NULL,
        related_name='main_product',
    )

    secondary_image = models.OneToOneField(
        to='product.ProductImage',
        on_delete=models.SET_NULL,
        related_name='secondary_product',
    )

    @property
    def related_products(self):
        related_products = Product.objects.filter(
            tags__in=self.tags.all()
        ).exclude(id=self.id)
        return related_products

    @property
    def all_images(self):
        from product.models import ProductImage
        return ProductImage.objects.filter(variant__product=self)

    @property
    def main_image_object(self):
        main_image = self.all_images.filter(main=True)
        if len(main_image) >= 1:
            return self.all_images.filter(main=True).first()
        return self.all_images.first()

    @property
    def lowest_variant_price(self):
        lowest_price = self.variants.all().aggregate(
            min_price=Min('price'),
        ).get('min_price', None)
        return '%.2f' % lowest_price if lowest_price else '0.00'

    @property
    def main_image(self):
        # return self.main_image_object.image.get_absolute_image_url
        try:
            main_image_object = self.main_image_object
            main_image = main_image_object.get_absolute_image_url
        except:
            main_image = None
        return main_image

    @property
    def get_total_review_count(self):
        review_count = self.review_set.filter(approved=True).count()
        return review_count

    @property
    def get_review_average_score(self):
        average_score = self.review_set.filter(
            approved=True,
        ).aggregate(Avg('score'))['score__avg']
        if average_score is not None:
            return f"{average_score:.1f}"
        return 0

    @property
    def variant_sku_list(self):
        variants = self.variants.filter(is_public=True)
        sku_list = [variant.sku for variant in variants]
        sku_list_str = '/'.join(sku_list)
        return sku_list_str

    @property
    def keywords_str(self):
        keywords = [keyword.name for keyword in self.keyword.all()]
        return '/'.join(keywords) if keywords else '-'

    @property
    def tags_str(self):
        tags = [tag.name for tag in self.tags.all()]
        return '/'.join(tags) if tags else '-'

    @property
    def types_str(self):
        types = [product_type.name for product_type in self.types.all()]
        return '/'.join(types) if types else '-'

    def __str__(self):
        return self.name
