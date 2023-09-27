from celery import Task, current_app

from user.services import ScheduledEmailsSender


class SendScheduledEmailsTask(Task):
    name = 'users.tasks.SendScheduledEmailsTask'

    def run(self):
        ScheduledEmailsSender().send_scheduled_emails()


current_app.register_task(SendScheduledEmailsTask())
