from calendar import timegm
from datetime import datetime


def convert_to_timestamp(datetime: datetime) -> int:
    return timegm(datetime.utctimetuple())
