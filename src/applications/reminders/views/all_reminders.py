from django.views.generic import TemplateView


class AllRemindersView(TemplateView):
    template_name = "reminders/all_reminders.html"
