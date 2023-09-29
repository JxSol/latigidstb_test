from django.contrib import admin
from django.contrib.admin import register

from .models import Order


@register(Order)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('customer', 'robot_serial')
