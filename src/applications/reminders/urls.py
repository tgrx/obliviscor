from django.urls import path

from applications.reminders.apps import RemindersConfig
from applications.reminders.views import AllRemindersView
from applications.reminders.views import ReminderCreateView
from applications.reminders.views import ReminderDeleteView
from applications.reminders.views import ReminderUpdateView
from applications.reminders.views import ReminderView

app_name = RemindersConfig.label

urlpatterns = [
    path("", AllRemindersView.as_view(), name="all_reminders"),
    path("r/<int:pk>/", ReminderView.as_view(), name="reminder"),
    path("r/<int:pk>/delete/", ReminderDeleteView.as_view(), name="delete"),
    path("r/<int:pk>/update/", ReminderUpdateView.as_view(), name="update"),
    path("r/create/", ReminderCreateView.as_view(), name="create"),
]
