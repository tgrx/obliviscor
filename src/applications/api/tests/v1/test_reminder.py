from datetime import timedelta
from os import urandom

from django.test import TestCase
from rest_framework import status

from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from project.utils.xdatetime import near
from project.utils.xdatetime import utcnow
from project.utils.xtests import ApiTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, ApiTestMixin, UserTestMixin):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/reminder/"
        self.user = self.create_user()
        self.token = self.create_auth_token(self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token}"}

        self.reminder = Reminder(creator=self.user)
        self.reminder.save()

    def test_user_get_anon(self):
        self.validate_response(
            self.endpoint, expected_status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_normal(self):
        self.validate_response(
            self.endpoint,
            headers=self.auth_headers,
            expected_response_payload=[
                {
                    "created_at": self.reminder.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "creator": self.user.pk,
                    "description": self.reminder.description,
                    "id": self.reminder.pk,
                    "location": self.reminder.location,
                    "notified_at": self.reminder.notified_at,
                    "notify_at": self.reminder.notify_at,
                    "participants": [],
                    "status": ReminderStatus.CREATED.name,
                    "title": self.reminder.title,
                },
            ],
        )

    def test_post_anon(self):
        self.validate_response(
            self.endpoint,
            method="post",
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_post_normal(self):
        placeholder = urandom(4).hex()
        title = f"title_{placeholder}"

        self.validate_response(
            self.endpoint,
            method="post",
            headers=self.auth_headers,
            data={"title": title,},
            expected_status_code=status.HTTP_201_CREATED,
        )

        reminders = Reminder.objects.filter(title=title)
        self.assertEqual(1, reminders.count())

        reminder = reminders.first()
        self.assertTrue(reminder)

        self.assertEqual(title, reminder.title)
        self.assertEqual(self.user, reminder.creator)
        self.assertTrue(near(utcnow(), reminder.created_at, 4))
        self.assertTrue(ReminderStatus.CREATED.name, reminder.status)

    def test_patch_anon(self):
        self.validate_response(
            f"{self.endpoint}{self.reminder.pk}/",
            method="patch",
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_patch_normal_title(self):
        rem = Reminder(creator=self.user, title="xxx")
        rem.save()

        self.validate_response(
            f"{self.endpoint}{rem.pk}/",
            method="patch",
            headers=self.auth_headers,
            data={"title": "yyy",},
            expected_status_code=status.HTTP_200_OK,
        )

        reminders = Reminder.objects.filter(title="yyy")
        self.assertEqual(1, reminders.count())

        reminder = reminders.first()
        self.assertTrue(reminder)

        self.assertEqual("yyy", reminder.title)
        self.assertEqual(rem.creator, reminder.creator)
        self.assertListEqual(
            list(rem.participants.all()), list(reminder.participants.all())
        )
        self.assertEqual(rem.pk, reminder.pk)

    def test_patch_normal_readonly(self):
        user2 = self.create_user()
        dtm = utcnow() - timedelta(days=1)

        dataset = {
            "created_at": dtm,
            "notified_at": dtm,
            "status": ReminderStatus.NOTIFIED.name,
            "creator": user2.pk,
        }

        old = {_f: getattr(self.reminder, _f) for _f in dataset}

        for field, value in dataset.items():
            self.validate_response(
                f"{self.endpoint}{self.reminder.pk}/",
                method="patch",
                headers=self.auth_headers,
                data={field: value},
                expected_status_code=status.HTTP_200_OK,
            )

        self.reminder.refresh_from_db()

        for field, expected_value in old.items():
            self.assertEqual(expected_value, getattr(self.reminder, field), field)

    def test_patch_not_own(self):
        user2 = self.create_user()
        rem = Reminder(creator=user2, title="xxx")
        rem.save()

        self.validate_response(
            f"{self.endpoint}{rem.pk}/",
            method="patch",
            headers=self.auth_headers,
            data={"title": "xxx"},
            expected_status_code=status.HTTP_403_FORBIDDEN,
        )

    def test_delete_anon(self):
        self.validate_response(
            f"{self.endpoint}{self.reminder.pk}/",
            method="delete",
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_normal(self):
        rem = Reminder(creator=self.user, title="xxx")
        rem.save()

        self.validate_response(
            f"{self.endpoint}{rem.pk}/",
            method="delete",
            headers=self.auth_headers,
            expected_status_code=status.HTTP_204_NO_CONTENT,
        )

        with self.assertRaises(Reminder.DoesNotExist):
            rem.refresh_from_db()
