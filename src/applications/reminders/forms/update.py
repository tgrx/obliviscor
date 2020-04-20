from django import forms

from applications.reminders.models import Reminder
from project.forms.fields import CustomDateTimeField
from project.utils.xmodels import a


class ReminderUpdateForm(forms.ModelForm):
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
            )
        ]

        widgets = {
            "title": forms.TextInput,
        }
