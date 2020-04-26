from applications.reminders.utils.consts import ReminderStatus
from periodic import tasks
from periodic.app import app
from periodic.utils.xmodels import get_reminder_model


@app.task
def notify_single_reminder(reminder_id) -> None:  # pragma: no cover
    print(f"BEGIN | {notify_single_reminder.__name__}")

    reminder_model = get_reminder_model()
    reminder = reminder_model.objects.get(pk=reminder_id)

    print(f"IN | {notify_single_reminder.__name__} | obtained {reminder}")

    if reminder.status != ReminderStatus.ENQUEUED.name:
        print(
            f"IN | {notify_single_reminder.__name__} | skipping {reminder.pk} due to status"
        )
        return

    emails = {
        reminder.creator.email,
    }
    emails.update(party.email for party in reminder.participants.all())

    print(
        f"IN | {notify_single_reminder.__name__} | {reminder} emails: {sorted(emails)}"
    )

    for email in emails:
        tasks.spam_reminder_party.delay(email, reminder.id)

    print(f"IN | {notify_single_reminder.__name__} | spam done")

    reminder.status = ReminderStatus.NOTIFIED.name
    reminder.save()

    print(f"IN | {notify_single_reminder.__name__} | {reminder}")

    print(f"END | {notify_single_reminder.__name__}")
