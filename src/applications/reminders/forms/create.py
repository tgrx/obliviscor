import delorean
from django import forms

from applications.reminders.models import Reminder
from project.forms.fields import CustomDateTimeField
from project.utils.xmodels import a


class ReminderCreateForm(forms.ModelForm):
    notify_at = CustomDateTimeField(required=True)

    class Meta:
        model = Reminder
        fields = [
            a(_f)
            for _f in (
                Reminder.notify_at,
                Reminder.title,
                Reminder.description,
                Reminder.location,
                Reminder.participants,
                Reminder.creator,
            )
        ]

        widgets = {
            "title": forms.TextInput,
            "creator": forms.HiddenInput,
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == "notify_at":
            value = delorean.Delorean().datetime
            return value
        return super().get_initial_for_field(field, field_name)
