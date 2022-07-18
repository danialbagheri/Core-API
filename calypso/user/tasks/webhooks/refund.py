from celery import Task

from user.services import ReviewReminderUndoService


class OrderRefundWebhookTask(Task):
    name = 'users.tasks.webhooks.refund'

    def run(self, refund_data):
        review_reminder_undo_service = ReviewReminderUndoService(refund_data)
        review_reminder_undo_service.undo_review_reminder()

