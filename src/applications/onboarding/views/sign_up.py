from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.onboarding.forms.sign_up import SignUpForm
from applications.onboarding.utils.verification import start_verification


class SignUpView(FormView):
    template_name = "onboarding/sign_up.html"
    form_class = SignUpForm

    def get_success_url(self):
        success_url = reverse_lazy("onboarding:sign_up_confirmed")
        return success_url

    @transaction.atomic()
    def form_valid(self, form):
        user = form.save()
        start_verification(self.request, user)
        return super().form_valid(form)
