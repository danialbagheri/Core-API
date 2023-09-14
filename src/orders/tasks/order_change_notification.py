from celery import Task, current_app

from orders.services import AmazonOrderSyncer


class OrderChangeNotificationTask(Task):
    name = 'orders.tasks.OrderChangeNotificationTask'

    def run(self, order_data):
        AmazonOrderSyncer(order_data).sync_order()


current_app.register_task(OrderChangeNotificationTask())
