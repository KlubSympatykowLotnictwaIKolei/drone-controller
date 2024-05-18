
from abc import ABC, abstractmethod
from typing import Callable

class MissionMessageChannel(ABC):
    """
    Interface for an object that is able to 
    send arbitrary bytes to the ground station.
    """

    @abstractmethod
    def send_message(self, message: bytes):
        pass