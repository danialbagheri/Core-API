from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.db.models import Q
from rest_framework.views import APIView
from .serializers import REASON_CHOICES, ContactFormSerializer, SliderSerializer,ConfigurationSerializer
from rest_framework import authentication, viewsets, generics
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from web.models import Slider, Configuration, SliderSlidesThroughModel
from web.instagram import get_user_feed
from product.models import Product, Tag, Keyword
from product.api.serializers import ProductSerializer
from sorl.thumbnail import get_thumbnail
from PIL import Image, ImageTk
from io import BytesIO
import requests
import os

class ContactForm(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    def post(self, request, *args, **kwargs):
        contact_serializer = ContactFormSerializer(
            data=request.data, context={"request": request})
        if contact_serializer.is_valid():
            data = contact_serializer.validated_data
            email_from = "admin@calypsosun.com"
            customer_email = data.get('email')
            subject = data.get('reason')
            query = data.get('message')
            message = f'''

From: {customer_email}


{query}
            '''

            try:
                if subject in REASON_CHOICES[:3]:
                    send_mail(subject, message, email_from, [
                              'pr@lincocare.com', 'info@calypsosun.com'],)
                else:
                    send_mail(subject, message, email_from,
                              ['info@calypsosun.com'],)
                return JsonResponse({"success": "Success"}, status=200)
            except Exception as e:
                return JsonResponse({"success": "Failed", "message": f"{e}"}, status=400)
        return JsonResponse(contact_serializer.errors, status=400)


class SliderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get('slug', False)
        if slug:
            queryset = queryset.filter(slug=slug)
        return queryset


class InstagramFeed(APIView):
    def get(self, request, *args, **kwargs):
        queryset = get_user_feed()
        for data in queryset:
            if data['media_type'] == "IMAGE" or data['media_type'] == "CAROUSEL_ALBUM":
                thumbnail, webp = self.reduce_photo_size(data['media_url'], data['id'])
                data["thumbnail"] = thumbnail
                data["webp"] = webp
        return JsonResponse(queryset, safe=False, status=200)

    def reduce_photo_size(self, url, id):
        current_site = Site.objects.get_current().domain
        media_root = str(settings.MEDIA_ROOT)
        path = "/instagram/calypso/"
        full_path = media_root + path + id + ".jpg"
        if os.path.isfile(full_path) is not True:
            r = requests.get(url)
            pilImage = Image.open(BytesIO(r.content))
            pilImage.save(f"{media_root}{path}{id}.jpg")
        image = current_site + get_thumbnail(full_path, '200x200', crop="center", quality=100, format="PNG").url
        webp = current_site + get_thumbnail(full_path, '200x200', crop="center", quality=100, format="WEBP").url
        return image, webp



class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    lookup_field = 'key'

# class HomePageView(viewsets.ReadOnlyModelViewSet):
#     serializer_class=HomePageSerializer

class Search(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = []
        query = self.request.query_params.get('q', None)
        if query is not None and len(query) >= 2:
            try:
                tag = Tag.objects.filter(Q(name__icontains=query)).first()
                keyword = Keyword.objects.filter(Q(name__icontains=query)).first()
                if tag is not None:
                    queryset = Product.objects.filter(Q(tags=tag)).distinct()
                elif keyword is not None:
                    queryset = Product.objects.filter(Q(keyword=keyword)).distinct()
                else:
                    queryset = Product.objects.filter(Q(name__icontains=query) | Q(sub_title__icontains=query) | Q(variants__sku__icontains=query)).distinct()
            except:
                pass
        return queryset