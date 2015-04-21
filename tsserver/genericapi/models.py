from tsserver import db
from tsserver.model import Model


class IMU(Model):
    """
    Model to store readings from IMU (inertial measurement unit).
    """
    timestamp = db.Column(db.DateTime, primary_key=True)

    # Output from gyro (16-bit per axis)
    gyro_x = db.Column(db.SmallInteger)
    gyro_y = db.Column(db.SmallInteger)
    gyro_z = db.Column(db.SmallInteger)

    # Output from accelerometer (12-bit per axis)
    accel_x = db.Column(db.SmallInteger)
    accel_y = db.Column(db.SmallInteger)
    accel_z = db.Column(db.SmallInteger)

    # Output from magnetometer (12-bit per axis)
    magnet_x = db.Column(db.SmallInteger)
    magnet_y = db.Column(db.SmallInteger)
    magnet_z = db.Column(db.SmallInteger)

    # Output from barometer (24-bit, 4096 LSb/mbar (hPa))
    pressure = db.Column(db.Integer)


class SHT(Model):
    """
    Model to store reading from SHT sensor (humidity + temperature).
    """
    timestamp = db.Column(db.DateTime, primary_key=True)

    # 0 to 100%, resolution 0.04%
    humidity = db.Column(db.Numeric(5, 2))

    # -40 to 125°C, resolution 0.01°C
    temperature = db.Column(db.Numeric(5, 2))


class GPS(Model):
    """
    Data from GPS.
    """
    timestamp = db.Column(db.DateTime, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # meters
    altitude = db.Column(db.Float)

    quality = db.Column(db.Enum('no_fix', 'gps', 'dgps'))

    # km/h
    speed_over_ground = db.Column(db.Float)

    # Dilution Of Precision
    fix_type = db.Column(db.Enum('no_fix', '2d', '3d'))
    pdop = db.Column(db.Float)
    hdop = db.Column(db.Float)
    vdop = db.Column(db.Float)

    # SmallInteger is kind of overkill, but SQLAlchemy does not support
    # TINYINTs...
    active_satellites = db.Column(db.SmallInteger)
    satellites_in_view = db.Column(db.SmallInteger)


class PlanetaryData(Model):
    """
    All data about the planet that is going to be calculated out of sensors'
    outputs (most of it after landing).
    """
    timestamp = db.Column(db.DateTime, primary_key=True)

    # kilograms
    planet_mass = db.Column(db.Float)
    # kilometers
    planet_radius = db.Column(db.Float)
    # g/cm³
    planet_density = db.Column(db.Float)

    # km/sec
    escape_velocity = db.Column(db.Float)

    earth_similarity_index = db.Column(db.Float)


class Status(Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    phase = db.Column(db.Enum('disconnected', 'launch_preparation',
                              'countdown', 'launch', 'descend',
                              'ground_operations', 'mission_complete'))


class GroundStationInfo(Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
