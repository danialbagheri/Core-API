from celery import Task, current_app

from orders.services.order_syncer import OrderSyncer


class OrderChangeNotificationTask(Task):
    name = 'orders.tasks.OrderChangeNotificationTask'

    def run(self, order_data):
        OrderSyncer(order_data).sync_order()


current_app.register_task(OrderChangeNotificationTask())
