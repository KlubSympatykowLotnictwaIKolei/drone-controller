
from dataclasses import dataclass
from typing import List
import numpy as np

import time

@dataclass
class HealthEventStats:
    last_event_timestamps: List[float]
    event_occurances: int

class LmaoHealthManager:
    """
    Class used for managing LMAO health. 
    It can monitor as many events as you want and it keeps track of 
    the frequency of events and how many times they have occured overall.
    """

    __MAX_COLLECTED_EVENT_TIMES = 10
    event_stats = {}

    def register_event_occurance(self, event_name: str):
        self.__register_event_if_not_exists(event_name)
        event = self.event_stats[event_name]

        event.last_event_timestamps = sorted([*event.last_event_timestamps, time.time()])[(-self.__MAX_COLLECTED_EVENT_TIMES):]
        event.event_occurances += 1

    def get_event_frequency(self, event_name: str) -> float:
        event = self.event_stats.get(event_name)

        if event is None:
            return 0
        
        timestamps = event.last_event_timestamps
        return (len(timestamps)-1) / (np.max(timestamps) - np.min(timestamps))
    
    def get_event_occurance_count(self, event_name: str) -> int:
        event = self.event_stats.get(event_name)

        if event is None:
            return 0
        
        return event.event_occurances

    def __register_event_if_not_exists(self, event_name: str):
        if self.event_stats.get(event_name) is not None:
            return
        
        self.event_stats[event_name] = HealthEventStats(
            last_event_timestamps=[time.time(), time.time() + 1],
            event_occurances=0,
        )

HEALTH_EVENT_SIGNAL = 'signal'
HEALTH_EVENT_DETECTION = 'detection'
HEALTH_EVENT_TELEMETRY = 'telemetry'

GLOBAL_HEALTH_MANAGER = LmaoHealthManager()