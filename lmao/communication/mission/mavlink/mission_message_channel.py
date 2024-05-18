
from ..mission_message_channel import MissionMessageChannel

from pymavlink.dialects.v20.ardupilotmega import MAVLink_encapsulated_data_message
from lmao.constants import LMAO_SYSTEM_ID, LMAO_COMPONENT_ID
from pymavlink import mavutil

import logging as log

class MavlinkMissionMessageChannel(MissionMessageChannel):
    """
    `MissionMessageChannel` implementation that sends 
    data through a mavlink connection.
    """
    
    def __init__(self, connection_string: str, baud: int = 115200, verbose: bool = False):
        self.connection = mavutil.mavlink_connection(
            connection_string, baud, 
            system_id=LMAO_SYSTEM_ID, 
            source_component=LMAO_COMPONENT_ID
        )
        log.info("Waiting MavLink for heartbeat...")
        self.connection.wait_heartbeat()
        log.info("Received heartbeat")

    def send_message(self, message: bytes):
        payload_size_bytes = len(message)
        bytes_to_send = bytes([payload_size_bytes])  # First byte - protobuf payload length
        bytes_to_send += message  # Protobuf payload
        bytes_to_send += bytes([0]) * (252 - payload_size_bytes)  # Padding bytes
        msg = MAVLink_encapsulated_data_message(0, bytes_to_send)
        self.connection.mav.send(msg)