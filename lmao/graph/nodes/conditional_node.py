from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.graph.nodes.null_node import NullNode

class ConditionalNode:

    def __init__(self, 
                 condition: callable, 
                 when_true: LmaoGraphNode = NullNode(), 
                 when_false: LmaoGraphNode = NullNode()):
        self.__condition = condition
        self.__true_node = when_true
        self.__false_node = when_false

    def process(self, signal: dict):
        if self.__condition(signal):
            self.__true_node.process(signal)
        else:
            self.__false_node.process(signal)

    def setup(self):
        self.__true_node.setup()
        self.__false_node.setup()

    def tear_down(self):
        self.__true_node.tear_down()
        self.__false_node.tear_down()