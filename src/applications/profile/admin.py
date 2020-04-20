from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.profile.models import Profile
from project.utils.xmodels import a


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {}


@admin.register(Profile)
class ProfileAdminModel(ModelAdmin):
    readonly_fields = [a(f) for f in (Profile.user,)]
