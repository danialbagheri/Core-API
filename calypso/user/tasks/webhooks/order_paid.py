from celery import Task, current_app

from user.services import ReviewReminderCreatorService


class OrderPaidWebhookTask(Task):
    name = 'users.tasks.webhooks.order_paid'

    def run(self, order_data):
        review_reminder_creator = ReviewReminderCreatorService(order_data)
        review_reminder_creator.create_review_reminder()


current_app.register_task(OrderPaidWebhookTask())
