from django.db.models import Q

from applications.reminders.utils.consts import ReminderStatus
from periodic import tasks
from periodic.app import app
from periodic.utils.xmodels import get_reminder_model
from project.utils.xdatetime import utcnow


@app.task
def notify_all_reminders():  # pragma: no cover
    print(f"BEGIN | {notify_all_reminders.__name__}")

    reminder_model = get_reminder_model()

    criteria = Q(status=ReminderStatus.CREATED.name)
    criteria &= Q(notify_at__lte=utcnow())
    criteria |= Q(status=ReminderStatus.ENQUEUED.name)

    reminders = reminder_model.objects.filter(criteria)

    print(f"IN | {notify_all_reminders.__name__} | reminders: {reminders.count()}")

    reminder_ids = set()

    for reminder in reminders:
        print(f"IN | {notify_all_reminders.__name__} | processing {reminder}")
        reminder.status = ReminderStatus.ENQUEUED.name
        reminder.save()
        reminder_ids.add(reminder.pk)
        print(f"IN | {notify_all_reminders.__name__} | enqueued {reminder}")

    for reminder_id in reminder_ids:
        tasks.notify_single_reminder.delay(reminder_id)
        print(
            f"IN | {notify_all_reminders.__name__} | sent {reminder_id} to processing"
        )

    print(f"END | {notify_all_reminders.__name__}")
