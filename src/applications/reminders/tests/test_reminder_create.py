from os import urandom

from django.test import Client
from django.test import TestCase

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from applications.reminders.views import ReminderCreateView
from applications.reminders.views import ReminderView
from project.utils.xdatetime import utcnow
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get_anonymous(self):
        self.validate_response(
            url=f"/r/create/",
            expected_status_code=200,
            expected_view=ReminderCreateView,
            expected_view_name="reminders:create",
            expected_template="reminders/form_create.html",
            content_filters=(lambda _c: b"Feel free to register" in _c,),
        )

    def test_get_user(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)

        client = Client()
        client.login(username=user.username, password=placeholder)

        self.validate_response(
            client=client,
            url=f"/r/create/",
            expected_view_name="reminders:create",
            expected_view=ReminderCreateView,
            expected_template="reminders/form_create.html",
            content_filters=(lambda _c: b"Feel free to register" not in _c,),
        )

    def test_post_user(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)

        client = Client()
        client.login(username=user.username, password=placeholder)

        dtm = utcnow()

        self.validate_response(
            client=client,
            method="post",
            url=f"/r/create/",
            form_data={
                "creator": user.pk,
                "status": ReminderStatus.NOTIFIED.name,
                "title": f"title_{placeholder}",
                "participants": [user.pk,],
            },
            expected_view_name="reminders:reminder",
            expected_view=ReminderView,
            expected_template="reminders/reminder.html",
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: f"title_{placeholder}".encode() in _c,
                lambda _c: ReminderStatus.CREATED.value.encode() not in _c,
                lambda _c: ReminderStatus.NOTIFIED.value.encode() not in _c,
            ),
        )

        qs = Reminder.objects.filter(creator=user)
        self.assertEqual(1, qs.count())

        rem = qs.first()
        self.assertTrue(rem)

        self.assertEqual(rem.creator, user)
        self.assertEqual(rem.created_at.year, dtm.year)
        self.assertEqual(rem.created_at.month, dtm.month)
        self.assertEqual(rem.created_at.day, dtm.day)
        self.assertEqual(rem.created_at.hour, dtm.hour)
        self.assertEqual(rem.created_at.minute, dtm.minute)
        self.assertEqual(rem.created_at.tzinfo, dtm.tzinfo)

        self.assertEqual(rem.title, f"title_{placeholder}")
        self.assertEqual(rem.status, ReminderStatus.CREATED.name)
        self.assertEqual(1, rem.participants.count())

        participant = rem.participants.first()
        self.assertEqual(participant, user)
