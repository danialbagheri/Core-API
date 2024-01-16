from celery import Task, current_app

from orders.services import AmazonOrderSyncer, AmazonOrderRetriever


class SyncAmazonOrdersTask(Task):
    name = 'orders.tasks.SyncAmazonOrdersTask'

    def run(self):
        orders = AmazonOrderRetriever().retrieve_orders()
        for order in orders:
            AmazonOrderSyncer(order).sync_order()


current_app.register_task(SyncAmazonOrdersTask())
