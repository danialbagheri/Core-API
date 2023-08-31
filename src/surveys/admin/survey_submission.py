from django.contrib import admin

from surveys.models import SurveySubmission
from surveys.models.survey_answer import SurveyAnswer


class SurveyAnswerInlineAdmin(admin.TabularInline):
    model = SurveyAnswer
    readonly_fields = ('question', 'choices', 'started_at', 'finished_at')
    extra = 0


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_name', 'email', 'submitted_at', 'started_at', 'finished_at', 'ip')
    readonly_fields = ('id', 'survey', 'email', 'user', 'ip', 'submitted_at', 'started_at', 'finished_at')
    list_filter = ('survey__name',)
    search_fields = ('email', 'ip',)
    inlines = (SurveyAnswerInlineAdmin,)

    def survey_name(self, survey_submission: SurveySubmission):
        return survey_submission.survey.name

    survey_name.short_description = 'Survey'
