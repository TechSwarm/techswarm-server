from tsserver import dtutils

timestamp = dtutils.datetime_from_str


def latitude(value):
    value = float(value)
    if value < -90 or value > 90:
        raise ValueError("Latitude is not in range [-90, 90]")
    return value


def longitude(value):
    value = float(value)
    if value < -180 or value > 180:
        raise ValueError("Latitude is not in range [-180, 180]")
    return value
