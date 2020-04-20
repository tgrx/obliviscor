from typing import Dict

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.profile.forms.profile_edit import ProfileEditForm

User = get_user_model()


class ProfileEditView(FormView):
    form_class = ProfileEditForm
    template_name = "profile/edit.html"
    success_url = reverse_lazy("profile:me")

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data["username"]
        user.save()

        profile = user.profile
        profile.name = form.cleaned_data["name"]
        profile.save()

        return super().form_valid(form)

    def get_initial(self) -> Dict:
        user = self.request.user
        initial = {}
        if not user.is_anonymous:
            initial.update(
                {
                    "username": user.username,
                    "name": user.profile.name if user.profile else "",
                }
            )
        return initial
