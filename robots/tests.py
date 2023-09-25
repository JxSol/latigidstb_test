from django.test import TestCase, Client
from django.urls import reverse

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


class TestCreateRobotView(TestCase):
    """Тест CreateRobotView."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('robots:create')

    def test_post_request(self):
        """Тест отправки POST-запроса."""
        response = self.client.post(
            path=self.url,
            data=r'{"model": "X5",'
                 r'"version": "LT",'
                 r'"created": "2023-01-01 00:00:01"}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Robot.objects.last().model, 'X5')
