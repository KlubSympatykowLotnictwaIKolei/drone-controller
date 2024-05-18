
from ..mission_message_channel import MissionMessageChannel
from pymavlink.dialects.v20.ardupilotmega import MAVLink_encapsulated_data_message
from lmao.constants import LMAO_SYSTEM_ID, LMAO_COMPONENT_ID

from pymavlink import mavutil

import redis

class RedisMissionMessageChannel(MissionMessageChannel):
    """
    MissionMessageChannel implementation for sending messages through Redis.
    This implementation sends messages to the `gs.send` pubsub channel.
    """

    def __init__(self, redis_host: str, output_channel_name: str = 'gs.send'):
        self.dummy_mavlink_connection = mavutil.mavlink_connection(
            'udpin:0.0.0.0:0', 
            source_system=1, 
            source_component=69
        )
        self.__output_channel_name = output_channel_name
        self.__redis_connection = redis.Redis(redis_host)

    def send_message(self, message: bytes):
        payload_size_bytes = len(message)
        bytes_to_send = bytes([payload_size_bytes])  # First byte - protobuf payload length
        bytes_to_send += message  # Protobuf payload
        bytes_to_send += bytes([0]) * (252 - payload_size_bytes)  # Padding bytes
        msg = MAVLink_encapsulated_data_message(0, bytes_to_send)

        bytes_to_send = msg.pack(self.dummy_mavlink_connection.mav)
        self.__redis_connection.publish(self.__output_channel_name, bytes_to_send)

    