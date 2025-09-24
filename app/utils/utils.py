from datetime import datetime


def now_datetime_with_timezone() -> datetime:
    return datetime.now().replace(tzinfo=None)
