from celery import Task, current_app

from user.services import ReviewReminderSender


class SendReviewReminderTask(Task):
    name = 'users.tasks.SendReviewReminderTask'

    def run(self):
        review_reminder_sender = ReviewReminderSender()
        review_reminder_sender.send_reminder_emails()


current_app.register_task(SendReviewReminderTask())
