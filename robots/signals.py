from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from orders.utils import notify_wait_list
from .models import Robot


@receiver(pre_save, sender=Robot)
def generate_serial(sender, instance, **kwargs):
    """Генерирует серийный номер для робота."""
    instance.serial = f"{instance.model}-{instance.version}"

@receiver(post_save, sender=Robot)
def notify_clients(sender, instance, created, **kwargs):
    """
    Посылает сигнал, что произвёлся новый робот.

    Здесь можно управлять логикой куда посылать уведомления, а куда нет.
    """
    if created:
        notify_wait_list(serial=instance.serial)  # лист ожидания

