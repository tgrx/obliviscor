from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

from applications.reminders.utils.consts import ReminderStatus
from project.utils.xdatetime import utcnow

User = get_user_model()


class Reminder(models.Model):
    created_at = models.DateTimeField(default=utcnow)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="own_reminders"
    )
    description = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    notify_at = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name="participated_reminders", blank=True
    )
    status = models.CharField(
        max_length=255,
        choices=ReminderStatus.to_choices(),
        default=ReminderStatus.CREATED.name,
    )
    title = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy("reminders:reminder", kwargs={"pk": str(self.pk)})
