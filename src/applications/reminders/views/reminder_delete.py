from django.urls import reverse_lazy
from django.views.generic import DeleteView

from applications.reminders.models import Reminder


class ReminderDeleteView(DeleteView):
    model = Reminder
    template_name = "reminders/form_delete.html"

    def get_success_url(self):
        return reverse_lazy("reminders:all_reminders")
