from rest_framework.generics import RetrieveAPIView

from ..serializers import SurveySerializer


class SurveyRetrieveAPIView(RetrieveAPIView):
    serializer_class = SurveySerializer
    lookup_field = 'slug'
