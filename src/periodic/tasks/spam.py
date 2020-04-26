from django.contrib.auth import get_user_model

from periodic.app import app
from periodic.utils.xmodels import get_reminder_model
from project.utils.safeguards import safe
from project.utils.xmail import send_email


@app.task
@safe
def spam_reminder_party(email: str, reminder_id: int) -> None:  # pragma: no cover
    print(f"BEGIN | {spam_reminder_party.__name__} | {email=}")

    reminder_model = get_reminder_model()
    user_model = get_user_model()

    reminder = reminder_model.objects.get(pk=reminder_id)
    user = user_model.objects.get(email=email)

    ok = send_email(
        context={"recipient": user, "reminder": reminder,},
        email_to=email,
        mail_template_name="notification",
        subject=f"Reminder about {reminder.title}",
    )

    print(f"IN | {spam_reminder_party.__name__} | spam {email=} {reminder_id=} {ok=}")
    print(f"END | {spam_reminder_party.__name__}")
