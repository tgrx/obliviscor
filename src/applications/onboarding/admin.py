from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.onboarding.models import AuthProfile
from project.utils.xmodels import a


class AuthProfileAdminForm(forms.ModelForm):
    class Meta:
        model = AuthProfile
        fields = "__all__"
        widgets = {}


@admin.register(AuthProfile)
class AuthProfileAdminModel(ModelAdmin):
    readonly_fields = [
        a(f)
        for f in (
            AuthProfile.user,
            AuthProfile.verification_code,
            AuthProfile.verified_at,
        )
    ]
