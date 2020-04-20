from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.reminders.forms import ReminderCreateForm
from applications.reminders.models import Reminder


class ReminderCreateView(CreateView):
    model = Reminder
    form_class = ReminderCreateForm
    template_name = "reminders/form_create.html"

    def get_success_url(self):
        return reverse_lazy("reminders:reminder", kwargs={"pk": str(self.object.pk)})

    def get_initial(self):
        return {
            "creator": self.request.user,
        }
