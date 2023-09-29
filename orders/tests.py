from django.test import TestCase

from .forms import OrderForm
from .models import Order


class OrderFormTestCase(TestCase):
    """Тест формы OrderForm."""
    def setUp(self):
        self.form_class = OrderForm
        self.fields = {
            'email': 'example@gmail.com',
            'robot_serial': 'R2-D2',
        }

    def test_model_create(self):
        """Тест создания модели через форму."""
        form = self.form_class(data=self.fields)
        form.is_valid()
        form.save(commit=True)
        self.assertTrue(
            Order.objects
            .filter(robot_serial=self.fields['robot_serial'])
            .exists()
        )
