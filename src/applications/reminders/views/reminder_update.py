from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.reminders.forms import ReminderUpdateForm
from applications.reminders.models import Reminder


class ReminderUpdateView(UpdateView):
    model = Reminder
    form_class = ReminderUpdateForm
    template_name = "reminders/form_update.html"

    def get_success_url(self):
        return reverse_lazy("reminders:reminder", kwargs={"pk": str(self.object.pk)})
