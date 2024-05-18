
from ..telemetry_source import TelemetrySource
from pymavlink import mavutil
import threading
import logging
import time

class MavLinkTelemetrySource(TelemetrySource):
    def __init__(self, connection_string: str, baud: int = 115200, system_id: int = 1, verbose: bool = False):
        self.connection = mavutil.mavlink_connection(connection_string, baud)
        logging.info("Waiting MavLink for heartbeat...")
        self.connection.wait_heartbeat()
        logging.info("Received heartbeat")

        threading.Thread(target=self.request_stream_rates, daemon=True).start()
        self.receiving_system_id = system_id

    def request_stream_rates(self):
        while True:
            self.connection.mav.command_long_send(
                self.connection.target_system, self.connection.target_component,
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
                33, # The MAVLink message ID (GLOBAL_POSITION_INT)
                1e6 / 16, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
                0, 0, 0, 0, # Unused parameters
                0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
            )

            self.connection.mav.command_long_send(
                self.connection.target_system, self.connection.target_component,
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
                30, # The MAVLink message ID (ATTITUDE)
                1e6 / 16, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
                0, 0, 0, 0, # Unused parameters
                0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
            )
            time.sleep(1)

    def receive_message(self):
        return self.connection.recv_match(blocking=True)
