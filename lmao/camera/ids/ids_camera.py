from ..camera_image_source import CameraImageSource

import logging as log
import numpy as np
import cv2

class IdsCameraImageSource(CameraImageSource):
    """
    camera image source for lmao.

    implementation for IDS UI-1240ML-C-HQ camera, should work for other IDS cameras. 

    Remember to install drivers: 
    https://en.ids-imaging.com/download-details/AB00182.html?os=linux_arm&version=v8&bus=64&floatcalc=hard#anc-software-309

    https://en.ids-imaging.com/files/downloads/ids-software-suite/readme/readme-ids-software-suite-linux-4.95.1_EN.html#installation


    1. Downlad debian package and unpack it
    !!! READ provided readme !!!
    2. remove all existing drivers - apt remove
    3. look inside /etc/ids, /opt/ids, and make sure there is nothing there otherwise installs will fail 
    4. start installig packages with ueye-common use apt install ./package_name.deb

    if error 10 encountered read carefully error messages 
    it should reead like file xxx already exists, remove it ig 


    when testing the camera use liveview, or when taking singular pictures wait for about 300 frames before actually saving it 

    i = 160
    # get data from camera and display
    lineinc = width * int((bitspixel + 7) / 8)
    while i > 0:
        img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
        img = np.reshape(img, (height, width, 3))
        i -= 1

    print(img)
    cv2.imwrite("aa.png", img) 

    """

    def __init__(self, width: int, height: int):

        from pyueye import ueye

        self.width = width
        self.height = height

        self.hcam = ueye.HIDS(0)
        ret = ueye.is_InitCamera(self.hcam, None)
        if ret != 0: log.error(f"initCamera returns {ret}") 
        else: log.info(f"initCamera returns {ret}")

        # set color mode
        ret = ueye.is_SetColorMode(self.hcam, ueye.IS_CM_BGR8_PACKED)
        if ret != 0: log.error(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")
        else: log.info(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")

        # enable auto exposure
        auto_exposure_enabled = ueye.INT(1)  # 1 enables auto exposure
        ret = ueye.is_SetAutoParameter(
            self.hcam, 
            ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, 
            auto_exposure_enabled, 
            ueye.sizeof(auto_exposure_enabled)
        )
        if ret != 0: log.error(f"SetAutoParameter IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER returns {ret}")
        else: log.info(f"SetAutoParameter IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER returns {ret}")

        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(0)
        rect_aoi.s32Y = ueye.int(0)
        rect_aoi.s32Width = ueye.int(width)
        rect_aoi.s32Height = ueye.int(height)
        ueye.is_AOI(self.hcam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
        if ret != 0: log.error(f"AOI IS_AOI_IMAGE_SET_AOI returns {ret}")
        else: log.info(f"AOI IS_AOI_IMAGE_SET_AOI returns {ret}")

        # allocate memory
        self.mem_ptr = ueye.c_mem_p()
        mem_id = ueye.int()
        self.bitspixel = 24 # for colormode = IS_CM_BGR8_PACKED
        ret = ueye.is_AllocImageMem(self.hcam, width, height, self.bitspixel,
                                    self.mem_ptr, mem_id)
        if ret != 0: log.error(f"AllocImageMem returns {ret}")
        else: log.info(f"AllocImageMem returns {ret}")

        # set active memory region
        ret = ueye.is_SetImageMem(self.hcam, self.mem_ptr, mem_id)
        if ret != 0: log.error(f"SetImageMem returns {ret}")
        else: log.info(f"SetImageMem returns {ret}")

        # continuous capture to memory
        ret = ueye.is_CaptureVideo(self.hcam, ueye.IS_DONT_WAIT)
        if ret != 0: log.error(f"CaptureVideo returns {ret}")
        else: log.info(f"CaptureVideo returns {ret}")
        
        # get data from camera and display
        self.lineinc = width * int((self.bitspixel + 7) / 8)

    def capture_image(self):
        img = ueye.get_data(self.mem_ptr, self.width, self.height, self.bitspixel, self.lineinc, copy=True)
        img = np.reshape(img, (self.height, self.width, 3))
        img = cv2.rotate(img, cv2.ROTATE_180) # FIXME: REMOVE AFTER SAE
        
        #TODO test if works on jetson 
        return img


    def disconnect(self):
        ret = ueye.is_StopLiveVideo(self.hcam, ueye.IS_FORCE_VIDEO_STOP)
        if ret != 0: log.error(f"StopLiveVideo returns {ret}")
        else: log.info(f"StopLiveVideo returns {ret}")
        
        ret = ueye.is_ExitCamera(self.hcam)
        if ret != 0: log.error(f"ExitCamera returns {ret}")
        else: log.info(f"ExitCamera returns {ret}") 
