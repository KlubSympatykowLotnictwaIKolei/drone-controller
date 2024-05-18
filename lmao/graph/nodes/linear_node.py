
from typing import Dict, List
from lmao.graph.lmao_graph_node import LmaoGraphNode


class LinearNode(LmaoGraphNode):
    """
    This node is meant to combine multiple nodes into one.
    When it processes a signal, it passes it through every one of its child nodes one by one, synchronously.
    """
    
    def __init__(self, nodes: List[LmaoGraphNode]):
        self.__nodes = nodes

    def setup(self):
        for node in self.__nodes:
            node.setup()

    def process(self, signal: Dict):
        for node in self.__nodes:
            node.process(signal)

    def tear_down(self):
        for node in self.__nodes:
            node.tear_down()