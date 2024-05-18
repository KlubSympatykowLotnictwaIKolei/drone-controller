
from typing import Dict, List
from lmao.graph.lmao_graph_node import LmaoGraphNode
from pprint import pprint

class SignalPrinterNode(LmaoGraphNode):
    """
    This is a debug node used for pretty printing the current value of the signal.
    """
    
    def __init__(self, skipped_keys: List[str] = []):
        self.__skipped_keys = skipped_keys
    
    def process(self, signal: Dict):
        signal_without_selected_keys = {key: signal[key] for key in signal if key not in self.__skipped_keys}
        pprint(signal_without_selected_keys)
