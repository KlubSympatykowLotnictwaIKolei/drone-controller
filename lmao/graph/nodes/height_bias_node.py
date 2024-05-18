

from typing import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode
from lmao.graph.nodes.telemetry_estimation_node import TelemetrySnapshot

class HeightBiasNode(LmaoGraphNode):
    """
    This node was created to add a slight bias to the UAV's height measurement.

    The Ardupilot's height measurement is relative to altitude at which the vehicle is armed. 
    When sitting on the ground, the UAV's relative height is 0 although the camera sits slightly above ground.
    HeightBiasNode node addressed this slight bias.
    """

    def __init__(self, bias: float, input_telemetry_key: str = 'telemetry') -> None:
        self.__bias = bias
        self.__input_telemetry_key = input_telemetry_key

    def process(self, signal: Dict):
        telemetry: TelemetrySnapshot = signal[self.__input_telemetry_key]
        telemetry.position.relative_altitude += self.__bias