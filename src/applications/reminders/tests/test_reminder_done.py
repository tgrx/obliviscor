from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from applications.onboarding.views import SignInView
from applications.reminders.models import Reminder
from applications.reminders.utils.consts import ReminderStatus
from applications.reminders.views import ReminderView
from project.utils.xtests import TemplateResponseTestMixin
from project.utils.xtests import UserTestMixin


class Test(TestCase, TemplateResponseTestMixin, UserTestMixin):
    def test_get(self):
        user = self.create_user()
        reminder = Reminder(creator=user, title=f"title_{user.username}")
        reminder.save()

        view_url = f"{reminder.get_absolute_url()}done/"
        sign_in_url = reverse_lazy("onboarding:sign_in")
        redirect_url = f"{sign_in_url}?next={view_url}"

        self.validate_response(
            url=view_url,
            expected_view_name="onboarding:sign_in",
            expected_view=SignInView,
            expected_redirect_chain=[(redirect_url, 302)],
            expected_template="onboarding/sign_in.html",
            content_filters=(lambda _c: b"error" not in _c,),
        )

    def test_post_anon(self):
        user = self.create_user()
        reminder = Reminder(creator=user, title=user.username)
        reminder.save()

        view_url = f"{reminder.get_absolute_url()}done/"
        sign_in_url = reverse_lazy("onboarding:sign_in")
        redirect_url = f"{sign_in_url}?next={view_url}"

        self.validate_response(
            method="post",
            url=view_url,
            expected_view_name="onboarding:sign_in",
            expected_view=SignInView,
            expected_redirect_chain=[(redirect_url, 302)],
            expected_template="onboarding/sign_in.html",
            content_filters=(lambda _c: b"error" not in _c,),
        )

    def test_post_user(self):
        user = self.create_user()
        client = Client()
        client.login(username=user.username, password=user.username)
        reminder = Reminder(creator=user, title=user.username)
        reminder.save()

        view_url = f"{reminder.get_absolute_url()}done/"

        self.validate_response(
            client=client,
            method="post",
            url=view_url,
            expected_view_name="reminders:reminder",
            expected_view=ReminderView,
            expected_redirect_chain=[(reminder.get_absolute_url(), 301)],
            expected_template="reminders/reminder.html",
            content_filters=(lambda _c: b"error" not in _c,),
        )

        reminder.refresh_from_db()

        self.assertEqual(reminder.status, ReminderStatus.DONE.name)
