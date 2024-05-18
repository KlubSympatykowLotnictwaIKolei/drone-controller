
from threading import Thread

import logging as log
import traceback
import signal
import os

class PanicOnErrorThread(Thread):
    """
    This class is meant to be used as a substitution for the normal `threading.Thread` class.
    When any unhandled error occurs it closes the whole application. 

    This is meant to prevent a situation in which one thread closes because of an error but others are still running.
    If the error crashes a thread that is critical for signal processing nothing can calculated, 
    but from the outside there would be little to no indication that something crashed.

    This implementation is meant to solve this problem by closing the whole application when anything crashes. 
    There should be ZERO unhandled errors in a properly running application, so when one occurs
    it must be bad. Thus, it is reasonable to shut everything down.
    """

    def __init__(self, **kwargs):
        Thread.__init__(self, daemon=True, **kwargs)

    def run(self):
        try:
            Thread.run(self)
        except Exception as unhandled_exception:
            log.error('Unhandled exception was thrown. Panicking!')
            print(traceback.format_exc())
            os.kill(os.getpid(), signal.SIGINT) # TODO: Check behaviour on Jetson