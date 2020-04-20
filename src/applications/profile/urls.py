from django.urls import path

from applications.profile.apps import ProfileConfig
from applications.profile.views import ProfileEditView
from applications.profile.views import ProfileView

app_name = ProfileConfig.label

urlpatterns = [
    path("", ProfileView.as_view(), name="me"),
    path("edit/", ProfileEditView.as_view(), name="edit"),
]
