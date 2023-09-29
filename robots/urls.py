from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.CreateRobotView.as_view(),
        name='create',
    ),
    path(
        'report/week/last',
        views.ProductionWeekReport.as_view(),
        name='week_report',
    ),

]