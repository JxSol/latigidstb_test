from django.core.mail import send_mail

from .models import Customer


def notify_customer(customer: Customer, message: str) -> None:
    """
    Отсылает уведомление клиенту.

    Здесь можно определить логику способа уведомления клиента.

    Params:
        - customer - клиент.
        - message - сообщение для клиента.
    """
    # отправим Email
    send_mail(
        subject="R4C: Ваш робот ждёт Вас!",
        message=message,
        from_email=None,
        recipient_list=[customer.email],
    )
