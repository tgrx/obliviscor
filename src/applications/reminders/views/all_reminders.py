from django.views.generic import TemplateView

from applications.reminders.models import Reminder


class AllRemindersView(TemplateView):
    template_name = "reminders/all_reminders.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return ctx

        ctx["own_reminders"] = Reminder.objects.filter(creator=self.request.user)
        ctx["participated_reminders"] = Reminder.objects.filter(
            participants__pk=self.request.user.id
        )

        return ctx
