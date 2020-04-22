from datetime import datetime
from unittest import TestCase

import pytz
from freezegun import freeze_time

from project.utils.xdatetime import now
from project.utils.xdatetime import utcnow


class Test(TestCase):
    @freeze_time("2020-01-02 13:45:00")
    def test_utcnow(self):
        dtm = utcnow()
        self.assertEqual(
            dtm,
            datetime(year=2020, month=1, day=2, hour=13, minute=45, tzinfo=pytz.UTC),
        )

    @freeze_time("2020-01-02 13:45:00")
    def test_now(self):
        tz = "Europe/Minsk"
        dtm = now(tz)
        expected = datetime(
            year=2020, month=1, day=2, hour=16, minute=45, tzinfo=pytz.timezone(tz)
        )

        self.assertEqual(expected.year, dtm.year)
        self.assertEqual(expected.month, dtm.month)
        self.assertEqual(expected.day, dtm.day)
        self.assertEqual(expected.hour, dtm.hour)
        self.assertEqual(expected.minute, dtm.minute)
