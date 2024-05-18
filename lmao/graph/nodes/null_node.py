
from lmao.graph.lmao_graph_node import LmaoGraphNode
from typing import Dict

class NullNode(LmaoGraphNode):
    """
    This node is used as a placeholder for a real node in order to avoid null checks in the code.
    Functionally it does nothing.
    """
    
    def setup(self):
        pass

    def process(self, signal: Dict):
        pass

    def tear_down(self):
        pass