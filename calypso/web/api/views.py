from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from rest_framework.views import APIView
from .serializers import REASON_CHOICES, ContactFormSerializer, SliderSerializer,ConfigurationSerializer
from rest_framework import authentication, viewsets
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from web.models import Slider, Configuration
from web.instagram import get_user_feed
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
            email_from = data.get('email')
            subject = data.get('reason')
            message = data.get('message')
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
        mobile = self.request.query_params.get('mobile', False)
        if slug:
            queryset = queryset.filter(slug=slug)
        if mobile and mobile.lower() == "true":
            queryset = queryset.filter(mobile=True)
        return queryset


class InstagramFeed(APIView):
    def get(self, request, *args, **kwargs):
        queryset = get_user_feed()
        for data in queryset:
            if data['media_type'] == "IMAGE" or data['media_type'] == "CAROUSEL_ALBUM":
                thumbnail = self.reduce_photo_size(data['media_url'], data['id'])
                data["thumbnail"] = thumbnail
        return JsonResponse(queryset, safe=False, status=200)

    def reduce_photo_size(self, url, id):
        current_site = Site.objects.get_current().domain
        media_root = settings.MEDIA_ROOT
        path = "/instagram/calypso/"
        full_path = media_root + path + id + ".jpg"
        if os.path.isfile(full_path):
            url_path = current_site + "/media"+ path + id + ".jpg"
        else:
            r = requests.get(url)
            pilImage = Image.open(BytesIO(r.content))
            pilImage.resize((100, 100), Image.ANTIALIAS)
            pilImage.save(f"{media_root}{path}{id}.jpg")
            url_path = current_site + "/media" +path + id + ".jpg"
        return url_path



class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration
    serializer_class = ConfigurationSerializer
    lookup_field = 'key'