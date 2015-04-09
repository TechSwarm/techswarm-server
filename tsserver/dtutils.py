"""
Datetime utils.
"""
from datetime import datetime

DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def datetime_to_str(datetime):
    """
    Serialize datetime provided as simplified ISO 8601 (without timezone)
    string

    :type datetime: datetime
    :param datetime: datetime object to convert to string
    :return: serialized datetime
    :rtype: str
    """
    return datetime.strftime(DT_FORMAT)


def datetime_from_str(str):
    """
    Deserialize datetime from simplified ISO 8601 (without timezone)
    :type str: str
    :param str: string to deserialize
    :return: datetime created of the string provided
    :rtype: datetime
    """
    return datetime.strptime(str, DT_FORMAT)


# For use with RequestParser as argument type
timestamp = datetime_from_str
