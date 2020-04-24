from datetime import timedelta

from django.test import Client
from django.test import TestCase

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from applications.reminders.views import ReminderUpdateView
from applications.reminders.views import ReminderView
from project.utils.xdatetime import utcnow
from project.utils.xtests import TemplateResponseTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, TemplateResponseTestMixin, UserTestMixin):
    def test_get_anonymous(self):
        user = self.create_user()

        rem = Reminder(creator=user, title=f"title_{user.username}")
        rem.save()

        self.validate_response(
            url="/r/update/",
            expected_status_code=404,
            content_filters=(lambda _c: b"Not Found" in _c,),
        )

        self.validate_response(
            url=f"/r/{rem.pk * 1000}/update/",
            expected_status_code=404,
            content_filters=(lambda _c: b"Not Found" in _c,),
        )

        self.validate_response(
            url=f"{rem.get_absolute_url()}update/",
            expected_status_code=200,
            expected_view=ReminderUpdateView,
            expected_view_name="reminders:update",
            expected_template="reminders/form_update.html",
            content_filters=(lambda _c: b"Feel free to register" in _c,),
        )

    def test_get_user(self):
        user = self.create_user()
        client = Client()
        client.login(username=user.username, password=user.username)

        rem = Reminder(creator=user, title=f"title_{user.username}")
        rem.save()

        self.validate_response(
            client=client,
            url=f"{rem.get_absolute_url()}update/",
            expected_view_name="reminders:update",
            expected_view=ReminderUpdateView,
            expected_template="reminders/form_update.html",
            content_filters=(lambda _c: f"title_{user.username}".encode() in _c,),
        )

    def test_post_user(self):
        user = self.create_user()
        client = Client()
        client.login(username=user.username, password=user.username)

        rem = Reminder(creator=user, title=user.username)
        rem.save()

        created_at = rem.created_at
        dtm = utcnow() + timedelta(days=1)

        self.validate_response(
            client=client,
            method="post",
            url=f"{rem.get_absolute_url()}update/",
            form_data={
                "created_at": dtm,
                "status": ReminderStatus.NOTIFIED,
                "title": f"title_{user.username}",
                "participants": [user.pk,],
            },
            expected_view_name="reminders:reminder",
            expected_view=ReminderView,
            expected_redirect_chain=[(rem.get_absolute_url(), 302)],
            expected_template="reminders/reminder.html",
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: f"title_{user.username}".encode() in _c,
                lambda _c: ReminderStatus.NOTIFIED.value.encode() not in _c,
            ),
        )

        rem.refresh_from_db()

        self.assertEqual(rem.title, f"title_{user.username}")
        self.assertEqual(rem.status, ReminderStatus.CREATED.name)
        self.assertEqual(rem.created_at, created_at)
        self.assertNotEqual(rem.created_at, dtm)
