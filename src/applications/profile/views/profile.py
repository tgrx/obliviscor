from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = "profile/me.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        req = self.request

        newbie = (req.GET or {}).get("newbie")
        if newbie:
            ctx["newbie_alert"] = " ".join(
                (
                    "We strongly encourage you to update your profile and password!",
                    "Your current password is the same as your current username.",
                    "Please copy the username, set the new one, and update the password.",
                )
            )

        return ctx
