from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.services import SPFFinderRecommender
from surveys.models import SurveySubmission
from ..serializers import SPFRecommendationVariantSerializer


class SPFRecommendationListAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = SPFRecommendationVariantSerializer

    def get_queryset(self):
        survey_submission_id = self.kwargs['survey_submission_id']
        survey_submission = get_object_or_404(SurveySubmission, id=survey_submission_id)
        return SPFFinderRecommender(survey_submission).get_recommended_variants()
