import os
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import JsonResponse
from rest_framework.views import APIView
from sorl.thumbnail import get_thumbnail

from web.instagram import get_user_feed


class InstagramFeed(APIView):

    def get(self, request, *args, **kwargs):
        queryset = get_user_feed()
        feed = []
        for data in queryset:
            single_post = {}
            if data['media_type'] == "IMAGE" or data['media_type'] == "CAROUSEL_ALBUM":
                thumbnail, webp = self.reduce_photo_size(data['media_url'], data['id'])
                single_post["thumbnail"] = thumbnail
                single_post["webp"] = webp
                single_post["caption"] = data["caption"]
                single_post["permalink"] = data["permalink"]
                single_post["id"] = data["id"]
                single_post["media_url"] = data["media_url"]
                single_post["media_type"] = data["media_type"]
                feed.append(single_post)
            else:
                pass
        return JsonResponse(feed, safe=False, status=200)

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
