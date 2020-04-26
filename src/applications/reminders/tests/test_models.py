from os import urandom

import delorean
from django.test import TestCase
from freezegun import freeze_time

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from project.utils.xtests import UserTestMixin


class Test(TestCase, UserTestMixin):
    @freeze_time("2019-01-02 03:45")
    def test_reminder_model(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)

        reminder = Reminder(creator=user)
        reminder.save()

        self.assertEqual(
            f"Reminder(pk={reminder.pk}, status=CREATED, notify_at=None, title=`None`)",
            str(reminder),
        )

        self.assertEqual("never", reminder.notify_at_full)
        self.assertEqual("never", reminder.notify_at_humanized)
        self.assertFalse(reminder.is_notified)
        self.assertFalse(reminder.is_done)

        dtm = delorean.parse("2020-01-02 03:45", timezone="UTC", dayfirst=False)
        reminder.notify_at = dtm.datetime
        reminder.save()

        self.assertEqual("03:45 at Thursday, January 02, 2020", reminder.notify_at_full)
        self.assertEqual("a year from now", reminder.notify_at_humanized)
        self.assertFalse(reminder.is_notified)
        self.assertFalse(reminder.is_done)

        reminder.status = ReminderStatus.NOTIFIED.name
        reminder.save()
        self.assertFalse(reminder.is_notified)
        self.assertFalse(reminder.is_done)

        reminder.notified_at = dtm.datetime
        reminder.save()
        self.assertTrue(reminder.is_notified)
        self.assertFalse(reminder.is_done)

        reminder.status = ReminderStatus.DONE.name
        reminder.save()
        self.assertFalse(reminder.is_notified)
        self.assertTrue(reminder.is_done)
