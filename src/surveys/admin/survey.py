from django.contrib import admin
from django.urls import resolve
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline

from surveys.models import Survey, SurveyQuestion, SurveyQuestionChoice


class SurveyQuestionChoiceInlineAdmin(SortableHiddenMixin,
                                      NestedTabularInline):
    model = SurveyQuestionChoice
    fk_name = 'question'
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if 'next_question' not in db_field.name:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        resolved = resolve(request.path_info)
        survey_id = resolved.kwargs['object_id'] if resolved.kwargs else None
        kwargs['queryset'] = SurveyQuestion.objects.filter(survey_id=survey_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SurveyQuestionInlineAdmin(SortableHiddenMixin,
                                NestedTabularInline):
    model = SurveyQuestion
    inlines = (SurveyQuestionChoiceInlineAdmin,)
    extra = 0


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    list_display = ('name',)

    inlines = (SurveyQuestionInlineAdmin,)
