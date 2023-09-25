from django.contrib import admin
from django.contrib.admin import register

from robots.models import Robot

@register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('serial', 'created')
    date_hierarchy = 'created'
