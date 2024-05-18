
from analysis.config.config import CommunicationChannelParameters, DetectorParameters, LiveViewParameters

from lmao.detection import StaticDetector, NullDetector, Detector
from lmao.communication import MavlinkMissionMessageChannel
from lmao.camera import StaticImageSource
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
from analysis.config.config import (
    CameraParameters,
    CommunicationChannelParameters,
    DetectorParameters,
    LiveViewParameters,
)

import logging as log

def create_detector_from_config(config: DetectorParameters) -> Detector:
    if config.type == "tensorrt":
        from lmao.detection.tensorrt import YoloV8TensorrtDetector

        return YoloV8TensorrtDetector(config.path)
    elif config.type == "ultralytics":
        from lmao.detection.ultralytics import YoloV8UltralyticsDetector

        return YoloV8UltralyticsDetector(config.path)
    elif config.type == "static":
        return StaticDetector()
    elif config.type == "none" or config.type is None or config.type == "null":
        log.warning("Using NULL detector")
        return NullDetector()
    else:
        log.error(f"Detector type '{config.type}' not recognized, using NULL detector")
        return NullDetector()



def create_telemetry_source_from_config(
    config: CommunicationChannelParameters,
) -> TelemetrySource:
    if config.type == "mavlink":
        telemetry_source = MavLinkTelemetrySource(config.address)
    elif config.type == "redis":
        telemetry_source = RedisTelemetrySource(config.address)
    elif config.type == "none" or config.type is None or config.type == "static":
        log.warning("Using STATIC telemetry source")
        telemetry_source = StaticTelemetrySource()
    else:
        log.error(
            f"Telemetry source type '{config.type}' not recognized, using STATIC telemetry source"
        )
        telemetry_source = StaticTelemetrySource()

    log.info("Awaiting a message from telemetry channel...")
    telemetry_source.receive_message()
    log.info("Message received")

    telemetry_source = TelemetrySourceIdFilter(telemetry_source, expected_system_id=1)
    return telemetry_source


def create_mission_channel_from_config(
    config: CommunicationChannelParameters,
) -> MissionMessageChannel:
    if config.type == "mavlink":
        return MavlinkMissionMessageChannel(config.address)  # NOT TESTED
    elif config.type == "redis":
        return RedisMissionMessageChannel(config.address)
    elif config.type == "none" or config.type is None or config.type == "null":
        log.warning("Using NULL mission message channel")
        return NullMissionMessageChannel()


def create_image_source_from_config(config: CameraParameters):
    if config.type == "airsim":
        from lmao.camera.airsim.airsim_camera import AirSimCameraSource
        return AirSimCameraSource()
    elif config.type == "pylon":
        from lmao.camera.pylon.pylon_camera import PylonCameraSource
        return PylonCameraSource(max_exposure_us=10000, target_fps=60, flip180=True)
    elif config.type == "ids":
        from lmao.camera.ids.ids_camera import IDSCameraSource
        return IDSCameraSource(width=1080, height=1024)
    elif config.type == "static":
        log.warning("Using STATIC image source")
        return StaticImageSource()
    else:
        log.error(
            f"Camera type '{config.type}' not recognized, using STATIC image source"
        )
        return StaticImageSource()
