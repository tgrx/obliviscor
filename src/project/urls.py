from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

urlpatterns = [
    # --- admin urls ---
    path("admin/", admin.site.urls),
    # --- applications ---
    path("", include("applications.reminders.urls")),
    path("o/", include("applications.onboarding.urls")),
    path("me/", include("applications.profile.urls")),
]

if settings.DEBUG and settings.PROFILING:  # pragma: no cover
    urlpatterns.append(re_path(r"^silk/", include("silk.urls", namespace="silk")))
