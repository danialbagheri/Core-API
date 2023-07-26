import os
from io import BytesIO
from typing import Tuple

import requests
from PIL import Image
from django.conf import settings
from django.contrib.sites.models import Site
from sorl.thumbnail import get_thumbnail

from . import InstagramImageThumbnailCreator


class InstagramImageLocalThumbnailCreator(InstagramImageThumbnailCreator):
    def get_image_path(self) -> str:
        media_root = settings.MEDIA_ROOT
        path = settings.INSTAGRAM_IMAGES_PATH
        return media_root + path + self.image_id + '.jpg'

    def image_exists(self, full_path: str) -> bool:
        return os.path.isfile(full_path)

    def upload_image(self, full_path: str) -> None:
        response = requests.get(self.image_url)
        pil_image = Image.open(BytesIO(response.content))
        pil_image.save(full_path)

    def create_thumbnails(self, full_path) -> Tuple[str, str]:
        current_site = Site.objects.get_current().domain
        png_url = current_site + get_thumbnail(full_path, '200x200', crop='center', quality=100, format='PNG').url
        webp_url = current_site + get_thumbnail(full_path, '200x200', crop='center', quality=100, format='WEBP').url
        return png_url, webp_url
