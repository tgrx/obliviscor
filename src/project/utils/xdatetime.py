from datetime import datetime
from typing import Optional

from delorean import Delorean
from django.conf import settings


def utcnow() -> datetime:
    return Delorean().datetime


def now(timezone: Optional[str] = None) -> datetime:
    tz = timezone or settings.TIME_ZONE
    return Delorean().shift(tz).datetime


def near(dt1: datetime, dt2: datetime, interval=0):
    delta = abs(dt1 - dt2)
    return delta.total_seconds() <= interval
