
from lmao.communication.telemetry.telemetry_interpolator import ATTITUDE, GLOBAL_POSITION_INT, GPS_RAW_INT, TelemetryInterpolator
from lmao.communication.telemetry.telemetry_source import TelemetrySource
from lmao.health.health_manager import GLOBAL_HEALTH_MANAGER, HEALTH_EVENT_TELEMETRY
from lmao.types import Attitude, PositionGPS
from lmao.graph.lmao_graph_node import LmaoGraphNode
from dataclasses import dataclass
from typing import Dict, Optional
import json
import logging as log
import threading


@dataclass
class TelemetrySnapshot:
    position: PositionGPS
    attitude: Attitude

class TelemetryEstimationNode(LmaoGraphNode):
    """
    This node reads telemetry in the background and when it processes a signal, 
    it tries to estimate the telemetry at a certain timestamp. 
    The estimated telemetry is stored in the signal.  
    """

    def __init__(self, 
                 telemetry_source: TelemetrySource,
                 input_timestamp_key: str = 'timestamp', 
                 output_key: str = 'telemetry'):
        self.__timestamp_key = input_timestamp_key
        self.__telemetry_source = telemetry_source
        self.__output_key = output_key

        self.__interpolator = TelemetryInterpolator()
        self.__position_received = threading.Event()
        self.__attitude_received = threading.Event()
        self.__raw_gps_received = threading.Event()


    def setup(self):
        self.__running = True
        self.__telemetry_thread = threading.Thread(target=self.telemetry_loop, daemon=True)
        self.__telemetry_thread.start()

        log.info("Waiting for GPS and attitude...")
        self.__position_received.wait()
        self.__raw_gps_received.wait()
        self.__attitude_received.wait()
        log.info("GPS and attitude received!")

    def process(self, signal: Dict):
        timestamp = signal[self.__timestamp_key]

        position = self.__interpolator.interpolate_position(self.__last_global_position_int, timestamp)

        signal[self.__output_key] = TelemetrySnapshot(
            position=position,
            attitude=self.__interpolator.interpolate_attitude(self.__last_attitude, timestamp)
        )

    def tear_down(self):
        self.__running = False
        del(self.__telemetry_thread)

    def telemetry_loop(self):
        while self.__running:
            msg = self.__telemetry_source.receive_message()

            if msg.get_type() == "ATTITUDE":
                GLOBAL_HEALTH_MANAGER.register_event_occurance(HEALTH_EVENT_TELEMETRY)
                self.__last_attitude = ATTITUDE.from_dict(msg)
                self.__attitude_received.set()

            if msg.get_type() == "GLOBAL_POSITION_INT":
                GLOBAL_HEALTH_MANAGER.register_event_occurance(HEALTH_EVENT_TELEMETRY)
                self.__last_global_position_int = GLOBAL_POSITION_INT.from_dict(msg)
                self.__position_received.set()

            if msg.get_type() == "GPS_RAW_INT":
                self.__last_gps_raw_int = GPS_RAW_INT.from_dict(msg)
                self.__raw_gps_received.set()