from django.db import transaction
from rest_framework import serializers

from common.services import RequestIPRetriever
from surveys.models import SurveySubmission, Survey
from .survey_answer import SurveyAnswerSerializer
from ...tasks import SendSurveyResultsEmailTask, SendSurveySubmissionNotificationEmailTask


class SurveySubmissionSerializer(serializers.ModelSerializer):
    survey = serializers.SlugRelatedField(slug_field='slug', queryset=Survey.objects.all())
    answers = serializers.ListSerializer(child=serializers.DictField(), write_only=True)

    class Meta:
        model = SurveySubmission
        fields = (
            'id',
            'survey',
            'answers',
            'email',
            'started_at',
            'finished_at',
        )
        read_only_fields = (
            'id',
        )

    def create_survey_answers(self, survey_submission, survey_answers_data):
        self.context['survey_submission'] = survey_submission
        for answer_data in survey_answers_data:
            serializer = SurveyAnswerSerializer(data=answer_data, context=self.context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def create(self, validated_data):
        validated_data['ip'] = RequestIPRetriever(request=self.context['request']).get_ip()
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
            validated_data['email'] = user.email
        survey_answers_data = validated_data.pop('answers')
        with transaction.atomic():
            survey_submission = super().create(validated_data)
            self.create_survey_answers(survey_submission, survey_answers_data)
        SendSurveyResultsEmailTask().delay(survey_submission.id)
        SendSurveySubmissionNotificationEmailTask().delay(survey_submission.id)
        return survey_submission
