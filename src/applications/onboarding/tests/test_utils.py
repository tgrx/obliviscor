from os import urandom
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from applications.onboarding.models import AuthProfile
from applications.onboarding.utils import verification
from project.utils import xmail

User = get_user_model()


class Test(TestCase):
    def test_setup_user_profile(self):
        placeholder = urandom(4).hex()
        user = User.objects.create_user(username=f"username_{placeholder}")
        auth = verification.setup_auth_profile(user)
        self.assertTrue(auth.verification_code)

    @patch.object(xmail, xmail.send_mail.__name__)
    def test_send_verification_email(self, mock_send_mail):
        placeholder = urandom(4).hex()
        request = Mock()
        request.site.domain = f"domain_{placeholder}"

        user = User.objects.create_user(
            email=f"email_{placeholder}", username=f"username_{placeholder}",
        )
        auth = AuthProfile(user=user, verification_code=f"vc_{placeholder}",)
        auth.save()

        verification.send_verification_email(request, auth)

        url = f"https://{request.site.domain}{auth.get_absolute_url()}"
        msg = f"""<p><a href="{url}">Verification link</a></p>"""

        mock_send_mail.assert_called_once_with(
            from_email=settings.EMAIL_FROM,
            html_message=msg,
            message=msg,
            recipient_list=[f"email_{placeholder}"],
            subject=f"Registration at Obliviscor",
        )

    def test_deactivate_user(self):
        placeholder = urandom(4).hex()
        user = User.objects.create_user(
            email=f"email_{placeholder}", username=f"username_{placeholder}",
        )
        self.assertTrue(user.is_active)

        verification.deactivate_user(user)
        self.assertFalse(user.is_active)

    @patch.object(xmail, xmail.send_mail.__name__)
    def test_start_verification(self, mock_send_mail):
        request = Mock()
        placeholder = urandom(4).hex()

        user = User.objects.create_user(
            email=f"email_{placeholder}", username=f"username_{placeholder}",
        )
        self.assertTrue(user.is_active)
        self.assertFalse(AuthProfile.objects.filter(user=user).all())

        verification.start_verification(request, user)

        self.assertFalse(user.is_active)

        auths = AuthProfile.objects.filter(user=user)
        self.assertEqual(auths.count(), 1)

        auth = auths.first()
        self.assertTrue(auth)
        self.assertEqual(auth.user, user)
        self.assertTrue(auth.verification_code)
        self.assertIsNone(auth.verified_at)
        self.assertFalse(auth.is_verified)

        mock_send_mail.assert_called_once()

    @patch.object(verification, verification.login.__name__)
    def test_finalize_verification(self, mock_login):
        placeholder = urandom(4).hex()
        request = HttpRequest()

        user = User.objects.create_user(
            email=f"email_{placeholder}",
            is_active=False,
            username=f"username_{placeholder}",
        )
        user.save()

        self.assertFalse(verification.finalize_verification(request, None))
        self.assertFalse(verification.finalize_verification(request, ""))
        self.assertFalse(
            verification.finalize_verification(request, f"vc_{placeholder}")
        )

        auth = AuthProfile(user=user, verification_code=f"vc_{placeholder}")
        auth.save()

        self.assertTrue(
            verification.finalize_verification(request, f"vc_{placeholder}")
        )

        user.refresh_from_db()
        auth.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(auth.verified_at)
        mock_login.assert_called_once_with(request, user)
