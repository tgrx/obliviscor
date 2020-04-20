from django.views.generic import DetailView

from applications.reminders.models import Reminder


class ReminderView(DetailView):
    template_name = "reminders/reminder.html"
    model = Reminder
