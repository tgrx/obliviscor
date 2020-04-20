from os import urandom
from unittest import TestCase

from django.contrib.auth import get_user_model

from applications.profile.utils.profile import setup_profile

User = get_user_model()


class Test(TestCase):
    def test_setup_profile(self):
        placeholder = urandom(4).hex()
        user = User.objects.create_user(username=f"username_{placeholder}")

        profile = setup_profile(None)
        self.assertFalse(profile)

        profile = setup_profile(user)
        self.assertTrue(profile)

        profile2 = setup_profile(user)
        self.assertTrue(profile2)

        self.assertEqual(profile, profile2)
