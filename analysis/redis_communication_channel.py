
from dataclasses import dataclass
from lmao.types import PositionGPS
import redis

@dataclass
class DetectionPositionOutgoingMessage:
    lat: float
    lon: float
    class_id: int 

class RedisCommunicationChannel:

    def __init__(self, redis_host: str = 'localhost'):
        self.__redis_connection = redis.Redis(redis_host)
        pubsub = self.redis_connection.pubsub()
        pubsub.subscribe('telemetry.receive')
        self.iterator = pubsub.listen()
        
    def receive(self):
        redis_message = next(self.iterator)
        while redis_message['type'] == 'subscribe':
            redis_message = next(self.iterator)
        
        return self.dummy_mavlink_connection.mav.parse_char(redis_message['data'])
    
    def send(self, pos: PositionGPS, class_id: int):
        pass