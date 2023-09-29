from django.urls import path

from . import views

urlpatterns = [
    path(
        'add/',
        views.CreateOrderView.as_view(),
        name='create',
    ),
    path(
        'add/success',
        views.order_created,
        name='created',
    ),
]
