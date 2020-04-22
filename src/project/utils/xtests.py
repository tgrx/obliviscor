from typing import Callable
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional

from delorean import Delorean
from django.contrib.auth import get_user_model
from django.test import Client

from applications.onboarding.models import AuthProfile
from applications.profile.models import Profile

User = get_user_model()


class ResponseTestMixin:
    def create_user(
        self, placeholder: str, user_kw: Optional[Dict] = None, verified=False
    ) -> User:
        form_data = {
            "username": f"username_{placeholder}",
            "email": f"email_{placeholder}@test.com",
            "password": placeholder,
        }

        user_kw = (user_kw or {}).copy()
        user_kw.update(form_data)

        user = User.objects.create_user(**user_kw)
        user.save()

        if verified:
            auth = AuthProfile(
                user=user,
                verification_code=placeholder,
                verified_at=Delorean().datetime,
            )
            auth.save()

        profile = Profile(user=user, name=f"name_{placeholder}")
        profile.save()

        return user

    def validate_response(
        self,
        *,
        url: str,
        client: Optional = None,
        method: Optional[str] = "get",
        form_data: Optional[Dict] = None,
        expected_status_code: Optional[int] = 200,
        expected_view: Optional[type] = None,
        expected_view_name: Optional[str] = None,
        expected_template: Optional[str] = None,
        content_filters: Optional[Collection[Callable[[bytes], bool]]] = None,
        expected_redirect_chain: Optional[List] = None,
    ):
        cli = client if client else Client()
        meth = getattr(cli, method)

        meth_args = []
        if form_data:
            meth_args.append(form_data)

        resp = meth(url, *meth_args, follow=True)
        self.assertEqual(expected_status_code, resp.status_code)

        if expected_redirect_chain is not None:
            self.assertEqual(expected_redirect_chain, resp.redirect_chain)

        good_resolver_codes = {
            200,
        }

        if expected_status_code in good_resolver_codes:
            self.assertEqual(expected_view_name, resp.resolver_match.view_name)
            self.assertEqual(
                expected_view.as_view().__name__, resp.resolver_match.func.__name__,
            )

            self.assertIn(expected_template, resp.template_name)

        for content_filter in content_filters or []:
            self.assertTrue(content_filter(resp.content))
