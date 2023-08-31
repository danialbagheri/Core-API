from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import SurveySubmissionSerializer


class SurveySubmissionCreateAPIView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = SurveySubmissionSerializer
