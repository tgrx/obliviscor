from os import urandom

from django.contrib.auth import get_user_model
from django.test import TestCase

from applications.onboarding.views import SignInView
from applications.profile.views import ProfileView
from applications.reminders.views import AllRemindersView
from project.utils.xtests import ResponseTestMixin

User = get_user_model()


class Test(TestCase, ResponseTestMixin):
    def test_sign_in_get(self):
        self.validate_response(
            url=f"/o/sign_in/",
            expected_view_name="onboarding:sign_in",
            expected_template="onboarding/sign_in.html",
            expected_view=SignInView,
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )

    def test_sign_in_post_success(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)

        form_data = {
            "username": user.username,
            "email": user.email,
            "password": placeholder,
        }

        self.validate_response(
            url=f"/o/sign_in/",
            method="post",
            form_data=form_data,
            expected_view_name="reminders:all_reminders",
            expected_template="reminders/all_reminders.html",
            expected_view=AllRemindersView,
            expected_redirect_chain=[("/", 302)],
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )

    def test_sign_in_post_failure_bad_creds(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder)

        form_data = {
            "username": user.username,
            "email": user.email,
            "password": placeholder * 2,
        }

        self.validate_response(
            url=f"/o/sign_in/",
            method="post",
            form_data=form_data,
            expected_view_name="onboarding:sign_in",
            expected_template="onboarding/sign_in.html",
            expected_view=SignInView,
            content_filters=(lambda _c: b"error" in _c,),
        )

    def test_signin_verified_success(self):
        placeholder = urandom(4).hex()
        self.create_user(placeholder, verified=True)

        self.validate_response(
            url=f"/o/sign_in/{placeholder}/",
            expected_view_name="profile:me",
            expected_template="profile/me.html",
            expected_view=ProfileView,
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
            expected_redirect_chain=[("/me/?newbie=1", 302)],
        )

    def test_signin_verified_failure_bad_code(self):
        placeholder = urandom(4).hex()
        self.create_user(placeholder, verified=True)

        self.validate_response(
            url=f"/o/sign_in/{placeholder * 2}/",
            expected_view_name="onboarding:sign_in",
            expected_template="onboarding/sign_in.html",
            expected_view=SignInView,
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )

    def test_signin_verified_failure_not_verified(self):
        placeholder = urandom(4).hex()
        self.create_user(placeholder)

        self.validate_response(
            url=f"/o/sign_in/{placeholder}/",
            expected_view_name="onboarding:sign_in",
            expected_template="onboarding/sign_in.html",
            expected_view=SignInView,
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )
