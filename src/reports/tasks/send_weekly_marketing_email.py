from celery import current_app, Task

from reports.services import WeeklyMarketingEmailService


class SendWeeklyMarketingEmailTask(Task):
    name = 'reports.tasks.SendWeeklyMarketingEmailTask'

    def run(self):
        weekly_marketing_email_service = WeeklyMarketingEmailService()
        weekly_marketing_email_service.send_email()


current_app.register_task(SendWeeklyMarketingEmailTask())
