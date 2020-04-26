from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus


class ReminderDoneView(LoginRequiredMixin, RedirectView):
    permanent = True
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):
        rem = get_object_or_404(Reminder, **self.kwargs)
        rem.status = ReminderStatus.DONE.name
        rem.save()
        return reverse_lazy("reminders:reminder", kwargs=self.kwargs)
