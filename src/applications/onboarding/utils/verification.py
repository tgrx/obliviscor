from os import urandom
from typing import Union

from delorean import Delorean
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import HttpRequest

from applications.onboarding.models import AuthProfile
from project.utils.consts import PROJECT_NAME
from project.utils.xmail import send_email

User = get_user_model()


def setup_auth_profile(user: User) -> AuthProfile:
    code = urandom(16).hex()  # FIXME: magic; not secure
    auth = AuthProfile(user=user, verification_code=code)
    auth.save()
    return auth


def send_verification_email(request: HttpRequest, auth: AuthProfile):
    domain = request.site.domain
    url = f"https://{domain}{auth.get_absolute_url()}"
    msg = f"""<p><a href="{url}">Verification link</a></p>"""

    send_email(
        html_message=msg,
        message=msg,
        recipients=[auth.user.email],
        subject=f"Registration at {PROJECT_NAME.capitalize()}",
    )


def deactivate_user(user):
    user.is_active = False
    user.save()


def start_verification(request: HttpRequest, user: User):
    auth = setup_auth_profile(user)
    send_verification_email(request, auth)
    deactivate_user(user)


def finalize_verification(request: HttpRequest, code: Union[str, None]) -> bool:
    if not code:
        return False

    try:
        auth = AuthProfile.objects.get(verification_code=code)
    except AuthProfile.DoesNotExist:
        return False

    auth.verified_at = Delorean().datetime
    auth.save()
    auth.user.is_active = True
    auth.user.save()

    login(request, auth.user)

    return True
