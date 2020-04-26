from datetime import datetime

import delorean
from django import forms
from django.conf import settings


class CustomDateTimeField(forms.DateTimeField):
    widget = forms.TextInput(attrs={"type": "datetime-local"})

    def validate(self, value):
        fixed_value = f"{value}:00"
        return super().validate(fixed_value)

    def to_python(self, value) -> datetime:
        if not value:
            return value
        parsed = delorean.parse(value, timezone=settings.TIME_ZONE, dayfirst=False)
        return parsed.datetime

    def prepare_value(self, value):
        if not isinstance(value, datetime):
            return super().prepare_value(value)

        dtm_utc = (
            delorean.Delorean(value, timezone=settings.TIME_ZONE).shift("UTC").datetime
        )
        dtm_super = super().prepare_value(dtm_utc)
        dtm_prepared = (
            delorean.Delorean(dtm_super, timezone=settings.TIME_ZONE)
            .shift(settings.TIME_ZONE)
            .datetime.replace(tzinfo=None)
            .strftime("%Y-%m-%dT%H:%M")
        )
        return dtm_prepared
