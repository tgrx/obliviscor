from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from applications.api.impl.v1.serializers import ReminderSerializer
from applications.api.impl.v1.serializers import UserSerializer
from applications.reminders.models import Reminder

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReminderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.creator != self.request.user:
            raise PermissionDenied("not your object")
        return super().perform_update(serializer)
