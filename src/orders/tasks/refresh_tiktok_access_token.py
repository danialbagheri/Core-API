from celery import Task, current_app

from common.services import TiktokClient


class RefreshTikTokAccessTokenTask(Task):
    name = 'orders.tasks.RefreshTikTokAccessTokenTask'

    def run(self):
        TiktokClient().refresh_access_token()


current_app.register_task(RefreshTikTokAccessTokenTask())
