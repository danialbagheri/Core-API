from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from product.services import SPFFinderRecommender
from product.services.spf_recommender_email import SPFRecommenderMailjetEmail
from surveys.models import SurveySubmission


class EmailSPFRecommendationAPIView(APIView):
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        if not email:
            return Response(data='No email received.', status=status.HTTP_400_BAD_REQUEST)
        survey_submission_id = self.request.data.get('survey_submission_id')
        survey_submission = get_object_or_404(SurveySubmission, id=survey_submission_id)
        variants = SPFFinderRecommender(survey_submission).get_recommended_variants()
        if not variants:
            return Response(data='No variants to recommend.', status=status.HTTP_200_OK)
        SPFRecommenderMailjetEmail(variants, emails=[email]).send_emails()
        return Response(data={}, status=status.HTTP_200_OK)
