
import math
import time

import numpy as np
from pydantic import BaseModel
from pyproj import Geod
from lmao.coordinate_calculation.bounding_box_to_gps_converter import PositionGPS
from lmao.types import Attitude

class GLOBAL_POSITION_INT(BaseModel):
    time_boot_ms: int
    lat: float
    lon: float
    alt: float
    relative_alt: float
    vx: float
    vy: float
    vz: float
    heading: float
    time_of_aqusition: float

    @classmethod
    def from_dict(cls, msg) -> "GLOBAL_POSITION_INT":
        global_position_received_timestamp = time.time()
        time_boot_ms = msg.time_boot_ms
        lat = msg.lat / 10e6
        lon = msg.lon / 10e6
        relative_alt = float(msg.relative_alt) / 1000.0
        alt = msg.alt / 1000.0
        heading = msg.hdg / 100.0
        vx = msg.vx / 100
        vy = msg.vy / 100
        vz = msg.vz / 100
        return cls(
            time_boot_ms=time_boot_ms,
            lat=lat,
            lon=lon,
            alt=alt,
            relative_alt=relative_alt,
            vx=vx,
            vy=vy,
            vz=vz,
            heading=heading,
            time_of_aqusition=global_position_received_timestamp,
        )
    
class GPS_RAW_INT(BaseModel):
    time_usec: int
    fix_type: int
    lat: float
    lon: float
    alt: float
    time_of_aquisition: float

    @classmethod
    def from_dict(cls, msg) -> 'GPS_RAW_INT':
        time_usec = msg.time_usec
        fix_type = msg.fix_type
        lat = msg.lat / 10e7
        lon = msg.lon / 10e7
        alt = (msg.alt/1000) - 212

        return cls(
            time_usec=time_usec,
            fix_type=fix_type,
            lat=lat,
            lon=lon,
            alt=alt,
            time_of_aquisition=time.time()
        )

class ATTITUDE(BaseModel):
    time_boot_ms: int
    roll: float
    pitch: float
    yaw: float
    rollspeed: float
    pitchspeed: float
    yawspeed: float
    time_of_aqusition: float

    @classmethod
    def from_dict(cls, msg) -> "ATTITUDE":
        global_position_received_timestamp = time.time()

        return cls(
            time_boot_ms=msg.time_boot_ms,
            roll=msg.roll,
            pitch=msg.pitch,
            yaw=msg.yaw,
            rollspeed=msg.rollspeed,
            pitchspeed=msg.pitchspeed,
            yawspeed=msg.pitchspeed,
            time_of_aqusition=global_position_received_timestamp,
        )
    
class TelemetryInterpolator:
    """
    Class that tries to estimate telemetry slightly before or after receiving the telemetry message.
    """

    def __init__(self, gps_delay = 0):
        self.__gps_delay = gps_delay

    def interpolate_attitude(self, attitude: ATTITUDE, target_timestamp) -> Attitude:
        attitude_delay = (
            self.__gps_delay + target_timestamp - attitude.time_of_aqusition
        )

        return Attitude(
            attitude.roll + (attitude.rollspeed  * attitude_delay),
            attitude.pitch + (attitude.pitchspeed * attitude_delay),
            attitude.yaw + (attitude.yawspeed   * attitude_delay),
        )
    
    def interpolate_position(self, gps: GLOBAL_POSITION_INT, target_timestamp) -> PositionGPS:
        gps_delay = (
            self.__gps_delay + target_timestamp - gps.time_of_aqusition
        )

        velocity_magnitude = math.sqrt(gps.vx**2 + gps.vy**2)
        velocity_direction = np.arctan2(gps.vy, gps.vx)
        longitude, latitude, _ = Geod(ellps="WGS84").fwd(
            lons=gps.lon,
            lats=gps.lat,
            az=velocity_direction / math.pi * 180,
            dist=velocity_magnitude * gps_delay
        )

        return PositionGPS(
            latitude,
            longitude,
            gps.relative_alt + gps.vz * gps_delay
        )