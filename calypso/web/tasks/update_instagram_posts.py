from celery import Task, current_app
from django.db import transaction

from product.models import ProductVariant
from web.instagram import get_user_feed
from web.models import InstagramPost
from web.utils import InstagramUtils


class UpdateInstagramPostsTask(Task):
    name = 'UpdateInstagramPosts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku_map = None

    def check_image_variants(self, instagram_post):
        caption = instagram_post.caption or ''
        caption_parts = caption.split(' ')
        variants_to_add = []
        for caption_part in caption_parts:
            if not caption_part.startswith('#'):
                continue
            sku = caption_part[1:]
            variant = self.sku_map.get(sku, None)
            if variant:
                variants_to_add.append(variant)
        if variants_to_add:
            instagram_post.variants.add(*variants_to_add)

    def run(self):
        variants = ProductVariant.objects.all()
        self.sku_map = {variant.sku: variant for variant in variants}
        with transaction.atomic():
            InstagramPost.objects.all().delete()
            images_data = get_user_feed()
            for image_data in images_data:
                if image_data['media_type'] not in ['IMAGE', 'CAROUSEL_ALBUM']:
                    continue
                thumbnail, webp = InstagramUtils.reduce_photo_size(image_data['media_url'], image_data['id'])
                instagram_post = InstagramPost.objects.create(
                    instagram_id=image_data['id'],
                    media_type=image_data['media_type'],
                    media_url=image_data['media_url'],
                    thumbnail=thumbnail,
                    webp=webp,
                    caption=image_data['caption'],
                    permalink=image_data['permalink'],
                )
                self.check_image_variants(instagram_post)


current_app.register_task(UpdateInstagramPostsTask())
