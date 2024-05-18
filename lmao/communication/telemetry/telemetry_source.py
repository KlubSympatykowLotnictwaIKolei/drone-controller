
from abc import ABC, abstractmethod

class TelemetrySource(ABC):
    @abstractmethod
    def receive_message(self) -> 'MavlinkMessage':
        pass