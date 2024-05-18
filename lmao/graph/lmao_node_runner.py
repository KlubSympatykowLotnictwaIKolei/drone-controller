
from lmao.graph.panic_on_error_thread import PanicOnErrorThread
from lmao.graph.lmao_graph_node import LmaoGraphNode

import logging as log

from lmao.health.health_manager import GLOBAL_HEALTH_MANAGER, HEALTH_EVENT_SIGNAL

RUNNER_STOP_TIMEOUT_SECONDS = 10

class LmaoNodeRunner:
    """
    Class used for running signal processing on a single LMAO Graph Node.
    When running, it generates signals and passes them to the node for processing.
    Signals are generated without any delay. 
    """
    
    def __init__(self, node: LmaoGraphNode):
        self.__node = node
        self.is_running = True
    
    def start(self):
        self.is_running = True
        log.info('Starting LMAO graph')

        setup_thread = PanicOnErrorThread(target=self.__run_setup)
        setup_thread.start()
        setup_thread.join()

        self.__thread = PanicOnErrorThread(target=self.__run_signal_loop)
        self.__thread.start()

    def stop(self):
        log.warning('Stopping LMAO graph...')
        self.is_running = False
        self.__thread.join(timeout=RUNNER_STOP_TIMEOUT_SECONDS)
        self.__node.tear_down()

    def __run_setup(self):
        self.__node.setup()
    
    def __run_signal_loop(self):
        counter = 0
        while self.is_running:
            GLOBAL_HEALTH_MANAGER.register_event_occurance(HEALTH_EVENT_SIGNAL)
            self.__node.process({'id': counter})
            counter += 1