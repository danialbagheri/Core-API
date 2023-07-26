from django.conf import settings

from . import InstagramImageThumbnailCreator
from .instagram_image_local_thumbnail_creator import InstagramImageLocalThumbnailCreator
from .instagram_image_s3_thumbnail_creator import InstagramImageS3ThumbnailCreator


class InstagramImageThumbnailCreatorFactory:
    @staticmethod
    def create_thumbnail_creator(image_url, image_id) -> InstagramImageThumbnailCreator:
        upload_to_cloud = settings.USE_S3
        if upload_to_cloud:
            return InstagramImageS3ThumbnailCreator(image_url, image_id)
        return InstagramImageLocalThumbnailCreator(image_url, image_id)
