from tsserver import db
from tsserver.model import Model


class Telemetry(Model):
    """
    All the data that is going to be obtained in regular time intervals
    (every second or so).
    """

    timestamp = db.Column(db.DateTime, primary_key=True)
    temperature = db.Column(db.Float)
    """Temperature in Celsius."""
    pressure = db.Column(db.Float)
    """Air pressure in hPa."""


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


class Status(Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    phase = db.Column(db.Enum('disconnected', 'launch_preparation',
                              'countdown', 'launch', 'descend',
                              'ground_operations', 'mission_complete'))


class GroundStationInfo(Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
