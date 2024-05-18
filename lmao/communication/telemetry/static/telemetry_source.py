
from lmao.communication.telemetry.telemetry_source import TelemetrySource
from pymavlink import mavutil
from itertools import cycle

import time

class StaticTelemetrySource(TelemetrySource):
    CONST_ATTITUDE_MESSAGE = mavutil.mavlink.MAVLink_attitude_message(
        time_boot_ms = 0,
        roll         = 0,
        pitch        = 0,
        yaw          = 0,
        rollspeed    = 0,
        pitchspeed   = 0,
        yawspeed     = 0,
    )

    CONST_GLOBAL_POSITION_INT_MESSAGE = mavutil.mavlink.MAVLink_global_position_int_message(
        time_boot_ms = 0,
        lat          = 511139344,
        lon          = 170643799,
        alt          = 100000,
        hdg          = 0,
        relative_alt = 15000,
        vx           = 0,
        vy           = 0,
        vz           = 0,
    )

    CONST_GPS_RAW_INT_MESSAGE = mavutil.mavlink.MAVLink_gps_raw_int_message(
        time_usec = 0,
        fix_type = 0,
        lat = 0,
        lon = 0,
        alt = (20+41) * 1e3,
        eph = 0,
        epv = 0,
        vel = 0,
        cog = 0,
        satellites_visible = 1,
    )


    def __init__(self, system_id: int = 1):
        self.CONST_ATTITUDE_MESSAGE.get_header().srcSystem = system_id
        self.CONST_GLOBAL_POSITION_INT_MESSAGE.get_header().srcSystem = system_id
        self.CONST_GPS_RAW_INT_MESSAGE.get_header().srcSystem = system_id

        self.__iterator = cycle([
            self.CONST_ATTITUDE_MESSAGE,
            self.CONST_GLOBAL_POSITION_INT_MESSAGE,
            self.CONST_GPS_RAW_INT_MESSAGE
        ])

    def receive_message(self) -> 'MavlinkMessage':
        time.sleep(0.5)
        return next(self.__iterator)
        