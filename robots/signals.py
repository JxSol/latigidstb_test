from django.db.models.signals import pre_save, pre_init
from django.dispatch import receiver

from .models import Robot


@receiver(pre_save, sender=Robot)
def generate_serial(sender, instance, **kwargs):
    """Генерирует серийный номер для робота."""
    instance.serial = f"{instance.model}-{instance.version}"
