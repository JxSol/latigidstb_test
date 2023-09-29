from django.shortcuts import render
from django.views.generic import CreateView

from .forms import OrderForm
from .models import Order


class CreateOrderView(CreateView):
    """Создаёт объекты заказов."""
    model = Order
    form_class = OrderForm
    success_url = 'success'

def order_created(request):
    """Успешное оформление заказа."""
    return render(request, 'orders/order_created.html')
