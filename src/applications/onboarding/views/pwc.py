from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


class PwcView(PasswordChangeView):
    template_name = "onboarding/pwc_form.html"

    def get_success_url(self):
        success_url = reverse_lazy("onboarding:pwc_done")
        return success_url
