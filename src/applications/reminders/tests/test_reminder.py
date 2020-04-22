from os import urandom

from django.test import Client
from django.test import TestCase

from applications.reminders.models import Reminder
from applications.reminders.views import ReminderView
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get_anonymous(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)
        rem = Reminder(creator=user, title=f"title_{placeholder}")
        rem.save()

        self.validate_response(
            url=f"/r/{rem.pk * 999}/",
            expected_status_code=404,
            content_filters=(lambda _c: b"Not Found" in _c,),
        )

        self.validate_response(
            url=rem.get_absolute_url(),
            expected_status_code=200,
            expected_view=ReminderView,
            expected_view_name="reminders:reminder",
            expected_template="reminders/reminder.html",
            content_filters=(lambda _c: b"Feel free to register" in _c,),
        )

    def test_get_user(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)
        rem = Reminder(creator=user, title=f"title_{placeholder}")
        rem.save()

        client = Client()
        client.login(username=user.username, password=placeholder)

        self.validate_response(
            client=client,
            url=rem.get_absolute_url(),
            expected_view_name="reminders:reminder",
            expected_view=ReminderView,
            expected_template="reminders/reminder.html",
            content_filters=(lambda _c: f"title_{placeholder}".encode() in _c,),
        )
