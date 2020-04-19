from datetime import timedelta

import delorean
from django.contrib.auth import get_user_model
from django.test import TestCase

from applications.onboarding.models import AuthProfile

User = get_user_model()


class Test(TestCase):
    def test_auth_profile(self):
        user = User.objects.create_user(username="xxx", email="xxx")

        auth = AuthProfile(user=user)
        auth.save()
        self.assertTrue(auth.pk)
        self.assertFalse(auth.is_verified)

        auth.verified_at = delorean.parse("2020-01-01").datetime
        auth.save()
        self.assertTrue(auth.is_verified)

        auth.verified_at = delorean.Delorean().datetime + timedelta(minutes=1)
        auth.save()
        self.assertFalse(auth.is_verified)

        self.assertEqual(
            str(auth), f"AuthProfile #{auth.pk} for 'xxx'",
        )
