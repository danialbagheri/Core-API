from celery import Task, current_app

from orders.services import OrderBuilder
from user.services import ReviewReminderCreatorService


class OrderPaidWebhookTask(Task):
    name = 'users.tasks.webhooks.order_paid'

    def run(self, order_data):
        review_reminder_creator = ReviewReminderCreatorService(order_data)
        review_reminder_creator.create_review_reminder()
        OrderBuilder(order_data).build()


current_app.register_task(OrderPaidWebhookTask())
