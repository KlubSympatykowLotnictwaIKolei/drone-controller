
from lmao.graph.panic_on_error_thread import PanicOnErrorThread
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.graph.nodes.null_node import NullNode
from typing import Dict, List

import queue

class ConcurrentBalancerNode(LmaoGraphNode):
    """
    This node is used to easily implement multithreaded balancing across nodes in the `balanced_nodes` list.

    When starting up, this node creates a separate thread for each of the balanced nodes.
    When it receives a signal, one of the nodes accepts it and processes it on its own thread.
    After that, it can be passed to the `post_balance_node`, for further, synchronised processing.

    #### Speed mismatching
    The case that more signals are being passed into this node than can be processed is handled gracefully.
    When such situation happens the `process()` funciton will simply block until one of the `balanced_nodes` finishes its processing
    and is ready to accept it. This way of handling speed mismatch ensures that only a limited number of signals 
    is present at any given moment and that memory usage will be predictable. 
    """
    
    def __init__(self, balanced_nodes: List[LmaoGraphNode], post_balance_node: LmaoGraphNode = NullNode()):
        self.__balanced_nodes = balanced_nodes
        self.__balance_input_queue = queue.Queue(len(balanced_nodes))
        self.__balance_output_queue = queue.Queue(1)
        self.__post_balance_node = post_balance_node
        self.__is_running = False
        self.__threads = []
    
    def setup(self):
        self.__setup_children_nodes()
        self.__create_processing_threads()

        self.__is_running = True
        for thread in self.__threads:
            thread.start()

    def process(self, signal: Dict):
        self.__balance_input_queue.put(signal)

    def tear_down(self):
        self.__is_running = False
        for thread in self.__threads:
            thread.join()
        
        self.__tear_down_children_nodes()

    def __run_balanced_thread(self, node: LmaoGraphNode):
        while self.__is_running:
            try:
                signal = self.__balance_input_queue.get(timeout=1)
            except queue.Empty:
                continue
            
            node.process(signal)
            
            signal_passed_on = False
            while not signal_passed_on:
                try:
                    self.__balance_output_queue.put(signal, timeout=1)
                    signal_passed_on = True
                except queue.Full:
                    if not self.__is_running:
                        break

    def __run_post_balance(self):
        while self.__is_running:
            try:
                signal = self.__balance_output_queue.get(timeout=1)
            except queue.Empty:
                continue

            self.__post_balance_node.process(signal)

    def __setup_children_nodes(self):
        for node in self.__balanced_nodes:
            node.setup()
        
        self.__post_balance_node.setup()

    def __create_processing_threads(self):
        self.__threads = []
        for node in self.__balanced_nodes:
            self.__threads.append(PanicOnErrorThread(
                target=self.__run_balanced_thread,
                args=(node, )
            ))
        self.__threads.append(PanicOnErrorThread(target=self.__run_post_balance))

    def __tear_down_children_nodes(self):
        for node in self.__balanced_nodes:
            node.tear_down()

        self.__post_balance_node.tear_down()