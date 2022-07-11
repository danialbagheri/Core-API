from celery import Task

from user.services import ReviewReminderCreatorService


class OrderPaidWebhookTask(Task):
    name = 'users.tasks.webhooks.order_paid'

    def run(self, order_data):
        ReviewReminderCreatorService.create_review_reminder(order_data)
