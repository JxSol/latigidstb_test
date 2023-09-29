from django import forms

from customers.models import Customer
from robots.validators import validate_robot_serial
from .models import Order


class OrderForm(forms.ModelForm):
    email = forms.EmailField()
    robot_serial = forms.CharField(
        max_length=5,
        validators=[validate_robot_serial]
    )

    class Meta:
        model = Order
        fields = (
            'email',
            'robot_serial',
        )
        labels = {
            'email': 'Email',
            'robot_serial': 'Серийный номер робота',
        }

    def save(self, commit=True):
        customer = (
            Customer.objects
            .filter(email=self.cleaned_data['email'])
            .first()
        )
        if not customer:
            customer = Customer.objects.create(
                email=self.cleaned_data['email'])
        self.instance.customer = customer
        return super().save(commit)
