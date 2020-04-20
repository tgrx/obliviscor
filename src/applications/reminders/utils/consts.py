import enum


@enum.unique
class ReminderStatus(enum.Enum):
    CREATED = "Created"
    ENQUEUED = "Enqueued"
    NOTIFIED = "Notified"
    DONE = "Done"

    @classmethod
    def to_choices(cls):
        return sorted((status.name, status.value) for status in cls)
