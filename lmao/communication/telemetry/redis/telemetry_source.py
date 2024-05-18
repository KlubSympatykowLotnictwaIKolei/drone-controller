
from ..telemetry_source import TelemetrySource
from pymavlink import mavutil

import redis

class RedisTelemetrySource(TelemetrySource):

    def __init__(self, host: str = 'localhost'):
        self.dummy_mavlink_connection = mavutil.mavlink_connection('udpin:0.0.0.0:0')
        self.redis_connection = redis.Redis(host)

        pubsub = self.redis_connection.pubsub()
        pubsub.subscribe('telemetry.receive')
        self.iterator = pubsub.listen()

    def receive_message(self) -> 'MavlinkMessage':
        redis_message = next(self.iterator)
        while redis_message['type'] == 'subscribe':
            redis_message = next(self.iterator)
        
        return self.dummy_mavlink_connection.mav.parse_char(redis_message['data'])