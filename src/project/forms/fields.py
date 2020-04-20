from datetime import datetime

import delorean
from django import forms
from django.conf import settings


class CustomDateTimeField(forms.DateTimeField):
    widget = forms.TextInput(attrs={"type": "datetime-local"})

    def validate(self, value):
        fixed_value = f"{value}:00"
        return super().validate(fixed_value)

    def to_python(self, value):
        return delorean.parse(value, timezone="Europe/Minsk").datetime

    def prepare_value(self, value):
        value = super().prepare_value(value)
        if isinstance(value, datetime):
            value = (
                delorean.Delorean(value, timezone=settings.TIME_ZONE)
                .shift("Europe/Minsk")
                .datetime.replace(tzinfo=None)
                .strftime("%Y-%m-%dT%H:%M")
            )
        return value
