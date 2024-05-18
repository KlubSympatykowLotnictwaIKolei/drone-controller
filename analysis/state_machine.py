
from transitions import Machine
from enum import Enum

INSPECTION_STATE_SCAN = 'SCAN'
INSPECTION_STATE_EXTRAORDINARY_EVENT = 'EVENT'
INSPECTION_STATE_REPORT_LAND = 'REPORT_LAND'

class StateMachine(object):
    """
    Main detection state machine, current state can be accessed with the .state attribute and changed using defined transitions.
    """

    states = [ INSPECTION_STATE_SCAN, INSPECTION_STATE_EXTRAORDINARY_EVENT, INSPECTION_STATE_REPORT_LAND ]
    transitions = [
        {
            'trigger':'detect_event',
            'source': INSPECTION_STATE_SCAN,
            'dest': INSPECTION_STATE_EXTRAORDINARY_EVENT
        }, # An event can be detected while searching
        {
            'trigger': 'report_land', 
            'source': '*',
            'dest': INSPECTION_STATE_REPORT_LAND
        }, # Report and land after the task is complete
        {
            'trigger': 'search_resume',
            'source': INSPECTION_STATE_EXTRAORDINARY_EVENT,
            'dest': INSPECTION_STATE_SCAN
        }
    ]

    def __init__(self):
        self.machine = Machine(
            model=self, 
            states=StateMachine.states,
            transitions=self.transitions,
            initial=INSPECTION_STATE_SCAN
        )

#TODO notes:
#   Should we only be able to go to report and land from search? (to wait untill handling an event is complete)