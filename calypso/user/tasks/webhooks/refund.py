from celery import Task, current_app

from user.services import ReviewReminderUndoService


class OrderRefundWebhookTask(Task):
    name = 'users.tasks.webhooks.refund'

    def run(self, refund_data):
        review_reminder_undo_service = ReviewReminderUndoService(refund_data)
        review_reminder_undo_service.undo_review_reminder()


current_app.register_task(OrderRefundWebhookTask())
