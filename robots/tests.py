from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from .models import Robot


class RobotModelTestCase(TestCase):
    def setUp(self):
        self.robot = Robot.objects.create(
            serial='R2-D2',
            model='R2',
            version='D2',
            created='2022-12-31 23:59:59',
        )

    def test_signal_generate_serial(self):
        """Тест сигнала generate_serial."""
        rob = Robot.objects.create(
            model='C3',
            version='PO',
            created='2022-12-31 23:59:59',
        )
        self.assertTrue(rob.serial == 'C3-PO')
