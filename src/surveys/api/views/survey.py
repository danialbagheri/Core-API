from rest_framework.generics import RetrieveAPIView

from surveys.models import Survey
from ..serializers import SurveySerializer


class SurveyRetrieveAPIView(RetrieveAPIView):
    serializer_class = SurveySerializer
    lookup_field = 'slug'
    queryset = Survey.objects.all()
