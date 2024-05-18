
from typing import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode

class ConstantValueNode(LmaoGraphNode):
    
    def __init__(self, constant_value, output_key: str):
        self.__constant_value = constant_value
        self.__output_key = output_key
    
    def process(self, signal: Dict):
        signal[self.__output_key] = self.__constant_value