from rest_framework import serializers

from surveys.models import SurveyQuestion
from . import SurveyQuestionChoiceSerializer


class SurveyQuestionSerializer(serializers.ModelSerializer):
    choices = SurveyQuestionChoiceSerializer(many=True)

    class Meta:
        model = SurveyQuestion
        fields = (
            'id',
            'text',
            'is_skippable',
            'has_multiple_answers',
            'choices',
        )
