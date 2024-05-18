
from abc import ABC, abstractmethod
from typing import Dict

class LmaoGraphNode(ABC):
    """
    LMAO Graph Node is a generic part of the LMAO signal processing system.

    #### process(signal)
    Each node must implement the `process` method. This method takes the signal (a dictionary)
    and applies its operations on it.

    #### setup() and tear_down()
    Each node can also implement the `setup` and `teardown` methods. 
    - `setup` is executed, before any signals begin to be processed. 
    - `tear_down` is executed before the application closes.

    These two methods were added for LMAO Graph Nodes that would require
    doing some book keeping besides just processing data

    #### Running
    Nodes can be run using the `LmaoNodeRunner`. 
    This class runs all the specific node methods at the appropriate time.
    """
    
    def setup(self):
        pass

    @abstractmethod
    def process(self, signal: Dict):
        pass

    def tear_down(self):
        pass