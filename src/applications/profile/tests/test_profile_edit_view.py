from os import urandom

from django.test import Client
from django.test import TestCase

from applications.profile.views import ProfileEditView
from applications.profile.views import ProfileView
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get_anonymous(self):
        self.validate_response(
            url="/me/edit/",
            expected_view_name="profile:edit",
            expected_view=ProfileEditView,
            expected_template="profile/edit.html",
            content_filters=(lambda _c: b"not authorized" in _c,),
        )

    def test_get_normal_user(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder, verified=True)
        client = Client()
        client.login(username=user.username, password=placeholder)

        self.validate_response(
            client=client,
            url="/me/edit/",
            expected_view_name="profile:edit",
            expected_view=ProfileEditView,
            expected_template="profile/edit.html",
            content_filters=(
                lambda _c: b"not authorized" not in _c,
                lambda _c: user.username.encode() in _c,
            ),
        )

    def test_profile_update(self):
        placeholder = urandom(4).hex()
        user = self.create_user(placeholder, verified=True)
        client = Client()
        client.login(username=user.username, password=placeholder)

        new_username = f"username_{placeholder}_xxx"
        new_name = f"name_{placeholder}_xxx"

        self.validate_response(
            client=client,
            url="/me/edit/",
            method="post",
            form_data={"username": new_username, "name": new_name},
            expected_view_name="profile:me",
            expected_view=ProfileView,
            expected_template="profile/me.html",
            content_filters=(
                lambda _c: b"not authorized" not in _c,
                lambda _c: new_name.encode() in _c,
                lambda _c: new_username.encode() in _c,
            ),
        )

        user.refresh_from_db()
        self.assertEqual(user.username, new_username)

        profile = user.profile
        profile.refresh_from_db()
        self.assertEqual(profile.name, new_name)
