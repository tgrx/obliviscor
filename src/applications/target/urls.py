from django.urls import path
from django.views.generic import TemplateView

from applications.target.apps import TargetConfig

app_name = TargetConfig.label

urlpatterns = [
    path("", TemplateView.as_view(template_name="target/index.html"), name="index"),
]
