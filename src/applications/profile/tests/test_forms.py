from os import urandom
from unittest import TestCase

from django.contrib.auth import get_user_model

from applications.profile.forms.profile_edit import ProfileEditForm
from project.utils.xtests import UserTestMixin

User = get_user_model()


class Test(TestCase, UserTestMixin):
    def test_profile_edit_form_empty(self):
        form = ProfileEditForm({})
        self.assertFalse(form.is_valid())

    def test_profile_edit_form_bad_username(self):
        form = ProfileEditForm({"username": ""})
        self.assertFalse(form.is_valid())

    def test_profile_edit_form_username_taken(self):
        user = self.create_user()

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
