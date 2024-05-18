
import time
from typing import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode

class WaitNode(LmaoGraphNode):
    """
    Node created mostly for debugging puposes. It sleeps for the provided number of seconds.
    """
    
    def __init__(self, time: float):
        self.__time = time

    def process(self, signal: Dict):
        time.sleep(self.__time)