from celery import Task, current_app

from orders.services import AmazonReviewReminderSender


class SendAmazonReviewReminderTask(Task):
    name = 'orders.tasks.SendAmazonReviewReminderTask'

    def run(self):
        review_reminder_sender = AmazonReviewReminderSender()
        review_reminder_sender.send_reminder_emails()


current_app.register_task(SendAmazonReviewReminderTask())
