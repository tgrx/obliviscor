from datetime import datetime
from typing import Optional

from delorean import Delorean
from django.conf import settings


def utcnow() -> datetime:
    return Delorean().datetime


def now(timezone: Optional[str] = None) -> datetime:
    tz = timezone or settings.TIME_ZONE
    return Delorean().shift(tz).datetime
