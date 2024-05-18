
from lmao.communication.telemetry.telemetry_source import TelemetrySource


class TelemetrySourceIdFilter(TelemetrySource):
    """
    Telemetry source decorator for filtering out unwanted messages from other drones
    """

    def __init__(self, telemetry_source: TelemetrySource, expected_system_id):
        self.__telemetry_source = telemetry_source
        self.__expected_system_id = expected_system_id

    def receive_message(self) -> 'MavlinkMessage':
        message = self.__telemetry_source.receive_message()

        while not message.get_srcSystem() == self.__expected_system_id:
            message = self.__telemetry_source.receive_message()

        return message