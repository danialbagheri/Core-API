from rest_framework import serializers

from surveys.models import SurveyQuestionChoice


class SurveyQuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionChoice
        fields = (
            'id',
            'text',
            'next_question',
        )
