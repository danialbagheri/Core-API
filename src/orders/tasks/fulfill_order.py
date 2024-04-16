from celery import Task, current_app

from orders.services import OrderFulfillmentService


class FulfillOrderTask(Task):
    name = 'orders.tasks.FulfillOrderTask'

    def run(self, order_data):
        OrderFulfillmentService(order_data).fulfill_order()


current_app.register_task(FulfillOrderTask())
