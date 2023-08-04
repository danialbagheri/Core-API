from rest_framework import serializers

from surveys.models import Survey
from . import SurveyQuestionSerializer


class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'slug',
            'email_required',
            'questions',
        )
