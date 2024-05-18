from analysis.launching.argument_parsing import parse_arguments
from analysis.launching.config_factory_functions import create_detector_from_config, create_image_source_from_config, create_mission_channel_from_config, create_telemetry_source_from_config
from analysis.state_machine import (
    StateMachine,
)
from analysis.nodes.time_machine_save_node import TimeMachineSaveNode
from analysis.config.config import (
    LmaoConfig,
    LmaoConfigLoader,
)

from lmao.coordinate_calculation.simple.simple_bounding_box_to_gps_converter import (
    SimpleBoundingBoxToGpsConverter,
)
from lmao.coordinate_calculation.screen_to_plane_position_converter import (
    ScreenToPlanePositionConverter,
)
from lmao.communication import MavlinkMissionMessageChannel
from lmao.coordinate_calculation import BoundingBoxToGpsConverter
from lmao.communication import (
    RedisMissionMessageChannel,
    NullMissionMessageChannel,
    TelemetrySourceIdFilter,
    MavLinkTelemetrySource,
    StaticTelemetrySource,
    MissionMessageChannel,
    RedisTelemetrySource,
    TelemetrySource,
)
from lmao.graph.nodes import (
    DetectionPositionCalculatorNode,
    TelemetryEstimationNode,
    ConcurrentBalancerNode,
    TelemetryEstimationNode,
    ConcurrentBalancerNode,
    SignalPrinterNode,
    ImageCaptureNode,
    TimeCaptureNode,
    DetectionNode,
    LinearNode,
    NullNode,
)
from lmao.graph import LmaoNodeRunner
from lmao.camera import CameraImageSource
from lmao.util.pretty_logging import setup_pretty_logging

from kink import di

import logging as log
import signal
import time

from albatros import UAV
from analysis.nodes.albatros_telemetry_node import AlbatrosTelemetryNode


setup_pretty_logging()

# uav = UAV(device="udpin:127.0.0.1:14550")

arguments = parse_arguments()
di[LmaoConfig] = LmaoConfigLoader().load_from_file(arguments.config_path)
di[TelemetrySource] = create_telemetry_source_from_config(di[LmaoConfig].communication.telemetry)
di[CameraImageSource] = create_image_source_from_config(di[LmaoConfig].camera)
di[MissionMessageChannel] = create_mission_channel_from_config(di[LmaoConfig].communication.mission)
di[ScreenToPlanePositionConverter] = ScreenToPlanePositionConverter()

state_machine = StateMachine()


runner = LmaoNodeRunner(
    LinearNode(
        [
            TimeCaptureNode(
                output_time_key="image_trigger_time",
            ),
            # AlbatrosTelemetryNode(
            #     uav,
            #     input_timestamp_key="image_trigger_time",
            #     output_key="telemetry",
            # ),
            TelemetryEstimationNode(
                input_timestamp_key="image_trigger_time",
                output_key="telemetry",
                telemetry_source=di[TelemetrySource]
            ),
            ImageCaptureNode(
                di[CameraImageSource],
                output_key="image",
            ),
            
            # TimeMachineSaveNode(),
        ]
    )
)

log.info("Starting runner")

signal.signal(signal.SIGINT, lambda _, __: runner.stop())
signal.signal(signal.SIGTERM, lambda _, __: runner.stop())

runner.start()

while runner.is_running:
    log.info("ITS ALIVE")
    time.sleep(1)
