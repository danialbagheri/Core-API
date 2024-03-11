from celery import Task, current_app

from product.services import SPFFinderRecommender
from surveys.models import SurveySubmission
from surveys.services import SurveyResultsMailjetEmail


class SendSurveyResultsEmailTask(Task):
    name = 'surveys.tasks.SendSurveyResultsEmailTask'

    def run(self, survey_submission_id):
        survey_submission = SurveySubmission.objects.filter(id=survey_submission_id).first()
        if not survey_submission:
            return
        recommended_variants = SPFFinderRecommender(survey_submission).get_recommended_variants()
        email = survey_submission.email
        SurveyResultsMailjetEmail(variants=recommended_variants, emails=[email]).send_emails()


current_app.register_task(SendSurveyResultsEmailTask())
