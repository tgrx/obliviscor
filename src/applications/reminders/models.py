from delorean import Delorean
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

from applications.reminders.utils.consts import ReminderStatus
from project.utils.xdatetime import utcnow

User = get_user_model()


class Reminder(models.Model):
    created_at = models.DateTimeField(default=utcnow)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="own_reminders", db_index=True
    )
    description = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    notify_at = models.DateTimeField(null=True, blank=True, db_index=True)
    participants = models.ManyToManyField(
        User, related_name="participated_reminders", blank=True, db_index=True
    )
    status = models.CharField(
        max_length=255,
        choices=ReminderStatus.to_choices(),
        default=ReminderStatus.CREATED.name,
        db_index=True,
    )
    title = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-notify_at", "-created_at"]

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"pk={self.pk},"
            f" status={self.status},"
            f" notify_at={self.notify_at},"
            f" title=`{self.title}`"
            f")"
        )

    def get_absolute_url(self):
        return reverse_lazy("reminders:reminder", kwargs={"pk": str(self.pk)})

    @property
    def notify_at_full(self) -> str:
        if not self.notify_at:
            return "never"
        return (
            Delorean(self.notify_at)
            .shift(settings.TIME_ZONE)
            .datetime.strftime("%H:%M at %A, %B %d, %Y")
        )

    @property
    def notify_at_humanized(self) -> str:
        if not self.notify_at:
            return "never"
        return Delorean(self.notify_at).humanize()

    @property
    def is_active(self):
        return (
            self.notify_at
            and self.notify_at >= utcnow()
            and not self.is_done
            and not self.notified_at
        )

    @property
    def is_notified(self):
        return bool(self.notified_at) and self.status == ReminderStatus.NOTIFIED.name

    @property
    def is_done(self):
        return self.status == ReminderStatus.DONE.name
