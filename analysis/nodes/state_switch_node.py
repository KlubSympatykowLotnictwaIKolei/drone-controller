from typing import Dict
from analysis import state_machine
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.graph.nodes.null_node import NullNode

class StateSwitchNode(LmaoGraphNode):
    """
    This node can switch between any amount of nodes based on the current state of the state machine.
    Specify a dictionary of states corresponding to each node.
    Optionally specify a default node to use if the current state is not in the dictionary, NullNode by default.
    """

    def __init__(self, state_machine: state_machine, nodes: Dict[str, LmaoGraphNode], default_node: LmaoGraphNode = NullNode()):
        self.__state_machine = state_machine
        self.__nodes = nodes
        self.__default_node = default_node

    def process(self, signal: dict):
        if self.__state_machine.state in self.__nodes:
            # If the current state  is in the expected dictionary, process the signal with the corresponding node
            self.__nodes[self.__state_machine.state].process(signal)
        else:
        # If the current state was not defined in the dictionary, use the default node.
        # null node by default, specify one unless you are sure the current state will always be in the dictionary or the signal should be ignored.
            self.__default_node.process(signal)
    
    def setup(self):
        #call setup on all children LmaoGraphNodes
        for node in self.__nodes.values():
            node.setup()
        # call setup on default node if it isn't in the dictionary
        if self.__default_node not in self.__nodes.values():
            self.__default_node.setup()

    def tear_down(self):
        #call tear_down on all children LmaoGraphNodes
        for node in self.__nodes.values():
            node.tear_down()
        # call tear_down on default node if it isn't in the dictionary
        if self.__default_node not in self.__nodes.values():
            self.__default_node.tear_down()

