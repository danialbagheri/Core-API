from rest_framework import serializers

from surveys.models import SurveyAnswer


class SurveyAnswerSerializer(serializers.ModelSerializer):
    choices = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = SurveyAnswer
        fields = (
            'id',
            'question',
            'choices',
            'started_at',
            'finished_at',
        )
        read_only_field = (
            'id',
        )

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        validated_data['submission'] = self.context['survey_submission']
        survey_answer = super().create(validated_data)
        survey_answer.choices.add(choices)
        return survey_answer
