from dataclasses import dataclass
from datetime import datetime
from typing import List

from common.services import BaseService
from surveys.models import SurveySubmission, SurveyAnswer


@dataclass
class SurveyAnswerInput:
    question_id: int
    choices: List[int]
    started_at: datetime
    finished_at: datetime


class SurveyAnswersCreator(BaseService):
    service_name = 'Survey Answers Creator'

    def __init__(self, survey_submission: SurveySubmission, answers_data: List[SurveyAnswerInput]):
        super().__init__(answers_data=answers_data)
        self.survey_submission = survey_submission
        self.answers_data = answers_data

    def create_answers(self):
        survey_answers_to_create = []
        survey_answer_choices_to_create = []

        for answer_data in self.answers_data:
            survey_answers_to_create.append(SurveyAnswer(
                submission=self.survey_submission,
                question_id=answer_data.question_id,
            ))
