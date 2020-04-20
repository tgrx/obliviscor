from os import urandom

from django.test import Client
from django.test import TestCase

from applications.reminders.views import AllRemindersView
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get_anonymous(self):
        self.validate_response(
            url="/",
            expected_view_name="reminders:all_reminders",
            expected_view=AllRemindersView,
            expected_template="reminders/all_reminders.html",
            content_filters=(lambda _c: b"Feel free to register" in _c,),
        )

    def test_get_registered(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder, verified=True)
        client = Client()
        client.login(username=user.username, password=placeholder)

        self.validate_response(
            url="/",
            client=client,
            expected_view_name="reminders:all_reminders",
            expected_view=AllRemindersView,
            expected_template="reminders/all_reminders.html",
            content_filters=(
                lambda _c: b"Feel free to register" not in _c,
                lambda _c: f"Welcome {user.profile.name}!".encode() in _c,
            ),
        )
