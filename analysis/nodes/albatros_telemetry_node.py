import time
from typing import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.graph.nodes.telemetry_estimation_node import TelemetrySnapshot
from albatros import UAV
from lmao.communication.telemetry.telemetry_interpolator import (
    ATTITUDE,
    GLOBAL_POSITION_INT,
    GPS_RAW_INT,
    TelemetryInterpolator,
)


class AlbatrosTelemetryNode(LmaoGraphNode):

    def __init__(
        self,
        albatros_connection: UAV,
        input_timestamp_key: str = "timestamp",
        output_key: str = "telemetry",
    ) -> None:
        self.__uav = albatros_connection
        self.__timestamp_key = input_timestamp_key
        self.__output_key = output_key
        self.__interpolator = TelemetryInterpolator()

    def process(self, signal: Dict):

        global_position_int = self.__uav.data.global_position_int
        global_position_int = GLOBAL_POSITION_INT(
            time_boot_ms=global_position_int.time_boot_ms,
            lat=global_position_int.lat / 10e6,
            lon=global_position_int.lon / 10e6,
            alt=global_position_int.alt / 1000.0,
            relative_alt=float(global_position_int.relative_alt) / 1000.0,
            vx=global_position_int.vx / 100,
            vy=global_position_int.vy / 100,
            vz=global_position_int.vz / 100,
            heading=global_position_int.hdg / 100.0,
            time_of_aqusition=time.time(),
        )


        att = self.__uav.data.attitude
        attitude = ATTITUDE(
            time_boot_ms=att.time_boot_ms,
            roll=att.roll,
            pitch=att.pitch,
            yaw=att.yaw,
            rollspeed=att.rollspeed,
            pitchspeed=att.pitchspeed,
            yawspeed=att.yawspeed,
            time_of_aqusition=time.time(),
        )

        timestamp = signal[self.__timestamp_key]

        position = self.__interpolator.interpolate_position(
            global_position_int, timestamp
        )

        signal[self.__output_key] = TelemetrySnapshot(
            position=position,
            attitude=self.__interpolator.interpolate_attitude(attitude, timestamp),
        )
