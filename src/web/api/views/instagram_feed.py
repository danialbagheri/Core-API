from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

from web.instagram import get_user_feed
from web.services import InstagramImageThumbnailCreatorFactory


class InstagramFeed(APIView):

    @method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):
        queryset = get_user_feed()
        feed = []
        for data in queryset:
            single_post = {}
            if data['media_type'] not in ['IMAGE', 'CAROuSEL_ALBUM']:
                continue
            thumbnail_creator = InstagramImageThumbnailCreatorFactory.create_thumbnail_creator(
                image_url=data['media_url'],
                image_id=data['id'],
            )
            png_url, webp_url = thumbnail_creator.get_image_thumbnails()
            single_post['thumbnail'] = png_url
            single_post['webp'] = webp_url
            single_post['caption'] = data['caption']
            single_post['permalink'] = data['permalink']
            single_post['id'] = data['id']
            single_post['media_url'] = data['media_url']
            single_post['media_type'] = data['media_type']
            feed.append(single_post)
        return JsonResponse(feed, safe=False, status=200)
