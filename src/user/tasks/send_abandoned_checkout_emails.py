from celery import Task, current_app

from user.services import AbandonedCheckoutRetriever, AbandonedCheckoutEmail


class SendAbandonedCheckoutEmailTask(Task):
    name = 'users.tasks.SendAbandonedCheckoutEmailTask'

    def run(self):
        checkouts = AbandonedCheckoutRetriever().get_checkouts()
        for checkout in checkouts:
            AbandonedCheckoutEmail(checkout).send_emails()


current_app.register_task(SendAbandonedCheckoutEmailTask())
