from django.test import Client
from django.test import TestCase

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from applications.reminders.views import AllRemindersView
from applications.reminders.views import ReminderDeleteView
from project.utils.xtests import TemplateResponseTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, TemplateResponseTestMixin, UserTestMixin):
    def test_get_anonymous(self):
        user = self.create_user()

        rem = Reminder(creator=user, title=f"title_{user.username}")
        rem.save()

        self.validate_response(
            url="/r/",
            expected_status_code=404,
            content_filters=(lambda _c: b"Not Found" in _c,),
        )

        self.validate_response(
            url=f"/r/{rem.pk * 1001}/delete/",
            expected_status_code=404,
            content_filters=(lambda _c: b"Not Found" in _c,),
        )

        self.validate_response(
            url=f"{rem.get_absolute_url()}delete/",
            expected_status_code=200,
            expected_view=ReminderDeleteView,
            expected_view_name="reminders:delete",
            expected_template="reminders/form_delete.html",
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
            url=f"{rem.get_absolute_url()}delete/",
            expected_view_name="reminders:delete",
            expected_view=ReminderDeleteView,
            expected_template="reminders/form_delete.html",
            content_filters=(lambda _c: f"title_{user.username}".encode() in _c,),
        )

    def test_post_user(self):
        user = self.create_user()

        rem = Reminder(creator=user, title=user.username)
        rem.save()

        client = Client()
        client.login(username=user.username, password=user.username)

        self.validate_response(
            client=client,
            method="post",
            url=f"{rem.get_absolute_url()}delete/",
            expected_view_name="reminders:all_reminders",
            expected_view=AllRemindersView,
            expected_redirect_chain=[("/", 302)],
            expected_template="reminders/all_reminders.html",
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: f"title_{user.username}".encode() not in _c,
                lambda _c: ReminderStatus.NOTIFIED.value.encode() not in _c,
            ),
        )

        with self.assertRaises(Reminder.DoesNotExist):
            rem.refresh_from_db()
