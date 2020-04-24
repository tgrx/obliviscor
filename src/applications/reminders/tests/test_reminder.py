from django.test import Client
from django.test import TestCase

from applications.reminders.models import Reminder
from applications.reminders.views import ReminderView
from project.utils.xtests import TemplateResponseTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, TemplateResponseTestMixin, UserTestMixin):
    def test_get_anonymous(self):
        user = self.create_user()
        rem = Reminder(creator=user, title=f"title_{user.username}")
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
        user = self.create_user()
        rem = Reminder(creator=user, title=f"title_{user.username}")
        rem.save()

        client = Client()
        client.login(username=user.username, password=user.username)

        self.validate_response(
            client=client,
            url=rem.get_absolute_url(),
            expected_view_name="reminders:reminder",
            expected_view=ReminderView,
            expected_template="reminders/reminder.html",
            content_filters=(lambda _c: f"title_{user.username}".encode() in _c,),
        )
