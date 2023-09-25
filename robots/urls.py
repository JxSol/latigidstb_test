from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.CreateRobotView.as_view(),
        name='create',
    ),
]