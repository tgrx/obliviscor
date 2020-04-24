from django.test import Client
from django.test import TestCase

from applications.reminders.views import AllRemindersView
from project.utils.xtests import TemplateResponseTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, TemplateResponseTestMixin, UserTestMixin):
    def test_get_anonymous(self):
        self.validate_response(
            url="/",
            expected_view_name="reminders:all_reminders",
            expected_view=AllRemindersView,
            expected_template="reminders/all_reminders.html",
            content_filters=(lambda _c: b"Feel free to register" in _c,),
        )

    def test_get_registered(self):
        user = self.create_user(verified=True)
        client = Client()
        client.login(username=user.username, password=user.username)

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
