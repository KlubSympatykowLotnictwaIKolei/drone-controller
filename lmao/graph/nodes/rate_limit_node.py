import time
from lmao.graph.lmao_graph_node import LmaoGraphNode

class RateLimitNode(LmaoGraphNode):
    """
    Node created for mock rate limiting purposes.
    It will always introduce some delay between processing signals.
    """

    def __init__(self, target_signals_per_second: int):
        """
        Args:
            target_signals_per_second: Desired signals per second. The number of signals that should be processed in one second.
                                        Works pretty acurate for less than 60 above that it starts to get a few percent off.
        
        """
        if target_signals_per_second <= 0:
            raise ValueError('FPS must be a positive number.')
        self.__target_delay = 1 / target_signals_per_second
        self.__last_time = 0

    def process(self, signal: dict):
        time_diff = time.time() - self.__last_time
        if time_diff < self.__target_delay:
            time.sleep(self.__target_delay - time_diff)
        self.__last_time = time.time()
