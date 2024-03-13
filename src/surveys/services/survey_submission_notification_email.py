from django.conf import settings

from common.services import MarketingEmailService
from surveys.models import SurveySubmission


class SurveySubmissionNotificationEmail(MarketingEmailService):
    subject = 'Survey Submission Notification'
    message = '''
An {survey_name} survey has been completed.

Results URL: {backend_url}/admin/surveys/surveysubmission/{survey_submission_id}/change/
'''
    service_name = 'Survey Submission Notification Email'

    def __init__(self, survey_submission: SurveySubmission):
        super().__init__(survey_submission_id=survey_submission.id)
        self.survey_submission = survey_submission

    def get_variables(self):
        return {
            'survey_name': self.survey_submission.survey.name,
            'backend_url': settings.BACKEND_ADDRESS,
            'survey_submission_id': self.survey_submission.id,
        }
