
from ..mission_message_channel import MissionMessageChannel

class NullMissionMessageChannel(MissionMessageChannel):
    """
    `MissionMessageChannel` implementation that does nothing.
    (Used for debugging)
    """

    def send_message(self, message: bytes):
        pass
