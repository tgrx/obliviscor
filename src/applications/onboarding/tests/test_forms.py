from os import urandom
from unittest import TestCase

from django.contrib.auth import get_user_model

from applications.onboarding.forms.sign_up import SignUpForm

User = get_user_model()


class Test(TestCase):
    def test_sign_up_form_empty(self):
        form = SignUpForm({})
        with self.assertRaises(ValueError):
            form.save()

    def test_sign_up_form_bad_email(self):
        form = SignUpForm({"email": ""})
        with self.assertRaises(ValueError):
            form.save()

        form = SignUpForm({"email": "xxx"})
        with self.assertRaises(ValueError):
            form.save()

    def test_sign_up_form_email_taken(self):
        placeholder = urandom(4).hex()
        user = User.objects.create_user(
            email=f"email_{placeholder}@test.com", username=f"username_{placeholder}",
        )

        form = SignUpForm({"email": user.email})
        with self.assertRaises(ValueError):
            form.save()

    def test_sign_up_form_success(self):
        placeholder = urandom(4).hex()
        email = f"email_{placeholder}@test.com"

        form = SignUpForm({"email": email})
        form.save()

        user = User.objects.filter(email=email)
        self.assertEqual(user.count(), 1)
        user = user.first()
        self.assertEqual(user.email, email)
        self.assertTrue(user.username)
        self.assertTrue(user.check_password(user.username))
