from django.urls import path

from applications.target.apps import TargetConfig
from applications.target.views import IndexView

app_name = TargetConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
