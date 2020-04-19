from delorean import Delorean
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class AuthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verification_code = models.CharField(max_length=255, unique=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_verified(self) -> bool:
        cond = self.verified_at and self.verified_at <= Delorean().datetime
        return cond

    def get_absolute_url(self) -> str:
        return reverse_lazy(
            "onboarding:sign_in_verified", kwargs={"code": self.verification_code}
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.pk} for {self.user.email!r}"
