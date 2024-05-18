
import time
from typing import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode

class TimeCaptureNode(LmaoGraphNode):
    """
    Node that captures current time and stores it in the signal.
    """
    
    def __init__(self, output_time_key: str):
        self.__output_time_key = output_time_key

    def process(self, signal: Dict):
        signal[self.__output_time_key] = time.time()
