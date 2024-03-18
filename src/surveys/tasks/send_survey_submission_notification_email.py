from celery import Task, current_app

from surveys.models import SurveySubmission
from surveys.services import SurveySubmissionNotificationEmail


class SendSurveySubmissionNotificationEmailTask(Task):
    name = 'surveys.tasks.SendSurveySubmissionNotificationEmailTask'

    def run(self, survey_submission_id: int):
        survey_submission = SurveySubmission.objects.filter(id=survey_submission_id).first()
        if not survey_submission:
            return

        SurveySubmissionNotificationEmail(survey_submission).send_email()
