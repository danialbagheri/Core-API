from rest_framework.generics import CreateAPIView

from user.api.serializers import VariantImageRequestSerializer


class VariantImageRequestCreateAPIView(CreateAPIView):
    serializer_class = VariantImageRequestSerializer
