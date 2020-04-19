from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from applications.onboarding.views import SignUpConfirmedView
from applications.onboarding.views import SignUpView
from project.utils import xmail
from project.utils.xtests import ResponseTestMixin

User = get_user_model()


class Test(TestCase, ResponseTestMixin):
    def test_sign_up_get(self):
        self.validate_response(
            url=f"/o/sign_up/",
            expected_view_name="onboarding:sign_up",
            expected_template="onboarding/sign_up.html",
            expected_view=SignUpView,
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )

    @patch.object(xmail, xmail.send_mail.__name__)
    def test_sign_up_post(self, mock_send_mail):
        form = {"email": "tesmail@test.com"}

        user = User.objects.filter(email=form["email"]).first()
        self.assertIsNone(user)

        self.validate_response(
            url=f"/o/sign_up/",
            method="post",
            form_data=form,
            expected_view_name="onboarding:sign_up_confirmed",
            expected_template="onboarding/sign_up_confirmed.html",
            expected_view=SignUpConfirmedView,
            expected_redirect_chain=[("/o/sign_up/confirmed/", 302)],
            content_filters=(
                lambda _c: b"error" not in _c,
                lambda _c: b"Error" not in _c,
            ),
        )

        mock_send_mail.assert_called_once()

        user = User.objects.get(email=form["email"])
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)
