from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from applications.onboarding.utils.verification import finalize_verification


class SignInVerifiedView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        code = self.kwargs.get("code")
        verified = finalize_verification(self.request, code)

        urls = (reverse_lazy("onboarding:sign_in"), settings.LOGIN_REDIRECT_URL)
        return urls[verified]
