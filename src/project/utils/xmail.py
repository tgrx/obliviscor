from typing import Collection

from django.conf import settings
from django.core.mail import send_mail


def send_email(
    recipients: Collection[str], subject: str, message: str, html_message: str,
):
    return send_mail(
        from_email=settings.EMAIL_FROM,
        html_message=html_message,
        message=message,
        recipient_list=list(recipients),
        subject=subject,
    )
