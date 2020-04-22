from datetime import datetime
from unittest import TestCase

import pytz
from django.core.exceptions import ValidationError

from project.forms.fields import CustomDateTimeField


class Test(TestCase):
    def test_custom_date_time_field_validate(self):
        f = CustomDateTimeField()
        try:
            f.validate("")
        except ValidationError as err:  # pragma: no cover
            self.assertFalse(err)

    def test_custom_date_time_field_to_python(self):
        tz = pytz.UTC

        f = CustomDateTimeField()
        d: datetime = f.to_python("2020-02-01T01:23")
        self.assertEqual(d.year, 2020)
        self.assertEqual(d.month, 2)
        self.assertEqual(d.day, 1)
        self.assertEqual(d.hour, 1)
        self.assertEqual(d.minute, 23)
        self.assertEqual(d.tzinfo, tz)

    def test_custom_date_time_field_prepare_value(self):
        f = CustomDateTimeField()

        tz = pytz.timezone("Europe/Minsk")
        d = datetime(
            year=2000,
            month=3,
            day=4,
            hour=5,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=tz,
        )

        s = f.prepare_value(d)
        self.assertEqual(s, "2000-03-04T03:10")

        s = f.prepare_value("xxx")
        self.assertEqual(s, "xxx")
