from django.db import models

from surveys.models import Survey


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    text = models.CharField(
        max_length=1024,
    )

    is_skippable = models.BooleanField()

    has_multiple_answers = models.BooleanField()

    position = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.text
