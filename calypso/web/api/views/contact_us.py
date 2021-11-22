from rest_framework.generics import CreateAPIView

from ..serializers import ContactFormSerializer


class ContactFormAPIView(CreateAPIView):
    serializer_class = ContactFormSerializer
