from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.reminders.models import Reminder
from project.utils.xmodels import a

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [a(_f) for _f in (User.id, User.email)]
        read_only_fields = [a(_f) for _f in (User.id, User.pk,)]


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"
        read_only_fields = [
            a(_f)
            for _f in (
                Reminder.created_at,
                Reminder.creator,
                Reminder.id,
                Reminder.notified_at,
                Reminder.pk,
                Reminder.status,
            )
        ]
