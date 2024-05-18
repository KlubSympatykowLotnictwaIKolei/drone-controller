
from typing import List
from lmao.communication.telemetry.telemetry_source import TelemetrySource
from lmao.graph.panic_on_error_thread import PanicOnErrorThread
from queue import Queue


class TelemetrySourceSplitter:
    """
    Class for allowing multiple threads to access the same telemetry source without race conditions 
    and similiar unwanted side-effects.
    """

    MAX_QUEUE_LENGTH = 16

    def __init__(self, telemetry_source: TelemetrySource):
        self.__telemetry_source = telemetry_source
        self.__split_telemetry_sources: List[self.SplitTelemetry] = []
        self.__thread = PanicOnErrorThread(target=self.__run_receive_loop)
        self.__thread.start()

    def split(self) -> TelemetrySource:
        new_split_source = self.SplitTelemetry()
        self.__split_telemetry_sources.append(new_split_source)
        return new_split_source

    def __run_receive_loop(self):
        while True:
            message = self.__telemetry_source.receive_message()
            
            for telemetry_source in self.__split_telemetry_sources:
                self.__add_message_to_queue(
                    telemetry_source.message_queue,
                    message,
                )

    def __add_message_to_queue(self, queue: Queue, message):
        if queue.qsize() >= self.MAX_QUEUE_LENGTH:
            queue.get()

        queue.put(message)

    class SplitTelemetry(TelemetrySource):
        message_queue = Queue()

        def receive_message(self) -> 'MavlinkMessage':
            return self.message_queue.get()