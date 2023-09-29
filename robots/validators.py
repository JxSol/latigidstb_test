from django.core.exceptions import ValidationError

from robots.messages import (
    INCORRECT_SERIAL_MASK,
    INCORRECT_MODEL_MASK,
    INCORRECT_VERSION_MASK
)


def validate_robot_serial(serial: str):
    """Проверяет правильность написания серийного номера робота."""
    splitted = serial.strip('-').split('-')
    if len(splitted) != 2:
        raise ValidationError(INCORRECT_SERIAL_MASK)
    model, version = splitted
    if len(model) != 2 or not model.isalnum():
        raise ValidationError(INCORRECT_MODEL_MASK)
    if not version.isalnum():
        raise ValidationError(INCORRECT_VERSION_MASK)
