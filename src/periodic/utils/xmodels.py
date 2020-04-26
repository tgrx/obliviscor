def get_auth_profile_model() -> type:  # pragma: no cover
    from applications.onboarding.models import AuthProfile as _Model

    return _Model


def get_reminder_model() -> type:  # pragma: no cover
    from applications.reminders.models import Reminder as _Model

    return _Model
