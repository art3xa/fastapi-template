import uuid
from calendar import timegm
from datetime import datetime


def convert_to_timestamp(datetime: datetime) -> int:
    return timegm(datetime.utctimetuple())


def generate_device_id() -> str:
    return str(uuid.uuid4())
