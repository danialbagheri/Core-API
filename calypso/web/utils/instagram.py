import os
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.contrib.sites.models import Site
from sorl.thumbnail import get_thumbnail


class InstagramUtils:
    @staticmethod
    def reduce_photo_size(url, _id):
        current_site = Site.objects.get_current().domain
        media_root = str(settings.MEDIA_ROOT)
        path = "/instagram/calypso/"
        full_path = media_root + path + _id + ".jpg"
        if os.path.isfile(full_path) is not True:
            r = requests.get(url)
            pil_image = Image.open(BytesIO(r.content))
            pil_image.save(f"{media_root}{path}{_id}.jpg")
        image = current_site + get_thumbnail(full_path, '200x200', crop="center", quality=100, format="PNG").url
        webp = current_site + get_thumbnail(full_path, '200x200', crop="center", quality=100, format="WEBP").url
        return image, webp
