from os import urandom
from unittest import TestCase

from django.contrib.auth import get_user_model

from applications.profile.forms.profile_edit import ProfileEditForm

User = get_user_model()


class Test(TestCase):
    def test_profile_edit_form_empty(self):
        form = ProfileEditForm({})
        self.assertFalse(form.is_valid())

    def test_profile_edit_form_bad_username(self):
        form = ProfileEditForm({"username": ""})
        self.assertFalse(form.is_valid())

    def test_profile_edit_form_username_taken(self):
        placeholder = urandom(4).hex()
        user = User.objects.create_user(
            email=f"email_{placeholder}@test.com", username=f"username_{placeholder}"
        )
        user.save()

        form_data = {"username": user.username}

        form = ProfileEditForm(form_data)
        self.assertFalse(form.is_valid())

        form = ProfileEditForm(form_data, initial=form_data)
        self.assertTrue(form.is_valid())

        new_form_data = form_data.copy()
        new_form_data["username"] *= 2

        form = ProfileEditForm(new_form_data, initial=form_data)
        self.assertTrue(form.is_valid())

        new_form_data = form_data.copy()
        new_form_data["name"] = "xxx"

        form = ProfileEditForm(new_form_data, initial=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_edit_form_success(self):
        placeholder = urandom(4).hex()
        form_data = {"username": placeholder}

        form = ProfileEditForm(form_data)
        self.assertTrue(form.is_valid())
