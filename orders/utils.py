from customers.utils import notify_customer
from orders.messages import WAIT_LIST_NEW_ROBOT
from orders.models import Order


def notify_wait_list(**kwargs) -> None:
    """
    Уведомляет лист ожидания о создании нового робота.

    Здесь можно определить логику рассылок по листу ожидания
    и выбрать сообщение.

    Params:
        - kwargs: контекстные данные.
    """
    order = Order.objects.filter(robot_serial=kwargs['serial']).first()
    if order:
        message = WAIT_LIST_NEW_ROBOT.format(kwargs['serial'].split('-'))
        notify_customer(order.customer, message)
        order.delete()
