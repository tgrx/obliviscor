from django.contrib import admin

from applications.reminders.models import Reminder


@admin.register(Reminder)
class ReminderAdminModel(admin.ModelAdmin):
    pass
