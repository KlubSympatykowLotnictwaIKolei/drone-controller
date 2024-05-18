import cv2

from .pylon_enums import PixelFormatValues, ExposureAutoValues
from ..camera_image_source import CameraImageSource

import logging as log

class PylonCameraImageSource(CameraImageSource):
    def __init__(self, target_fps: float, min_exposure_us: int = 1, max_exposure_us: int = None, timeout_us: int = 1000000, flip180: bool = False):
        from pypylon import pylon
        
        self.timeout = timeout_us
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        self.camera.Open()

        max_exposure_time_to_enable_target_fps_us = 1e6 / target_fps 

        if max_exposure_us is None:
            max_exposure_us = max_exposure_time_to_enable_target_fps_us

        if max_exposure_us > max_exposure_time_to_enable_target_fps_us:
            log.warning('Specified max exposure time may decrease fps below target')

        self.__initialize_auto_brightness(min_exposure_us, max_exposure_us)
        self.__initialize_proper_pixel_format()
        self.__set_desired_frame_rate(target_fps)
        
        self.camera.ReverseX.Value = flip180
        self.camera.ReverseY.Value = flip180
        self.__bayer_to_color_converter_enum = cv2.COLOR_BAYER_RG2RGB if not flip180 else cv2.COLOR_BAYER_RG2BGR

        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        log.info(f'Expected camera FPS: {self.camera.ResultingFrameRate.Value}')

    def disconnect(self):
        self.camera.StopGrabbing()
        self.camera.Close()

    def capture_image(self):
        # timeout - important, because it also limits exposure time
        # if we set this too low, upper limit does not matter because exposure ends on timeout

        img = None

        if self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(self.timeout, pylon.TimeoutHandling_Return)
        if not grabResult.IsValid():
            return None

        if grabResult.GrabSucceeded():
            img = grabResult.Array  # ndarray
            img = cv2.cvtColor(img, self.__bayer_to_color_converter_enum)

        grabResult.Release()
        return img

    def __initialize_auto_brightness(self, min_exposure_us, max_exposure_us):
        self.camera.AutoGainLowerLimit.Value = 0
        self.camera.AutoGainUpperLimit.Value = 10
        self.camera.GainAuto.Value = "Continuous"

        self.camera.AutoExposureTimeLowerLimit = min_exposure_us
        self.camera.AutoExposureTimeUpperLimit = max_exposure_us
        self.camera.ExposureAuto.Value = "Continuous"

        self.camera.AutoTargetBrightness.Value = 0.15
        self.camera.AutoFunctionROISelector.Value = "ROI1"
        self.camera.AutoFunctionROIUseBrightness.Value = True
        self.camera.AutoFunctionProfile.Value = "MinimizeExposureTime"
    
    def __initialize_proper_pixel_format(self):
        self.camera.ReverseX.Value = False
        self.camera.ReverseY.Value = False

        self.camera.PixelFormat.Value = "BayerRG8"

    def __set_desired_frame_rate(self, target_fps):
        self.camera.AcquisitionFrameRateEnable.SetValue(True)
        self.camera.AcquisitionFrameRate.SetValue(target_fps)