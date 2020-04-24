from django.test import TestCase

from applications.profile.views import ProfileView
from project.utils.xtests import TemplateResponseTestMixin


class Test(TestCase, TemplateResponseTestMixin):
    def test_get(self):
        self.validate_response(
            url="/me/",
            expected_view_name="profile:me",
            expected_view=ProfileView,
            expected_template="profile/me.html",
        )
