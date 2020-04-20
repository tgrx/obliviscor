from datetime import datetime

from delorean import Delorean
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

from applications.reminders.utils.consts import ReminderStatus

User = get_user_model()


def _now() -> datetime:
    return Delorean().datetime


class Reminder(models.Model):
    created_at = models.DateTimeField(default=_now)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="own_reminders"
    )
    description = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    notify_at = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participated_reminders",)
    status = models.CharField(
        max_length=255,
        choices=ReminderStatus.to_choices(),
        default=ReminderStatus.CREATED,
    )
    title = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy("reminders:reminder", kwargs={"pk": str(self.pk)})
