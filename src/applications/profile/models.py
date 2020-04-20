from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="profile"
    )
    name = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.pk} for {self.user.email!r}"
