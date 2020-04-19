from django.urls import path

from applications.onboarding.apps import OnboardingConfig
from applications.onboarding.views import IndexView
from applications.onboarding.views import PwcDoneView
from applications.onboarding.views import PwcView
from applications.onboarding.views import SignInVerifiedView
from applications.onboarding.views import SignInView
from applications.onboarding.views import SignOutView
from applications.onboarding.views import SignUpConfirmedView
from applications.onboarding.views import SignUpView

app_name = OnboardingConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("pwc/", PwcView.as_view(), name="pwc"),
    path("pwc/done/", PwcDoneView.as_view(), name="pwc_done",),
    path("sign_in/", SignInView.as_view(), name="sign_in",),
    path("sign_in/<str:code>/", SignInVerifiedView.as_view(), name="sign_in_verified",),
    path("sign_out/", SignOutView.as_view(), name="sign_out",),
    path("sign_up/", SignUpView.as_view(), name="sign_up"),
    path("sign_up/confirmed/", SignUpConfirmedView.as_view(), name="sign_up_confirmed"),
]
