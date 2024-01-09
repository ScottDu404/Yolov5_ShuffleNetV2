# -*- coding: utf-8 -*-
"""
@Time : 2022-09-03 17:07
@Auth : NopainMea
@File :acq_rgb.py
@IDE :PyCharm
@E-mail : 3284346435@qq.com
"""

from get_depth.acquisition import BaseAcquisition
import cv2
import numpy as np


class AcqRgb(BaseAcquisition):
    def __init__(self, camera_id):
        super(AcqRgb, self).__init__()
        self.camera_id = camera_id
        pass

    def _to__grey(self):
        pass


class AstraProRgb(AcqRgb):
    def __init__(self, camera_id=0):
        super(AstraProRgb, self).__init__(camera_id)
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        self.frame = None
        pass

    def _to__grey(self):
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def img_reshape(self, shape):
        self.frame = cv2.resize(self.frame, shape)
        return self.frame

    def acq_image(self):
        ret, self.frame = self.cap.read()
        return self.frame

    def cam_visualize(self, windows_name='rgb'):
        while int(cv2.waitKey(1)) != ord('q'):
            self.acq_image()
            cv2.imshow(windows_name, self.frame)


if __name__ == '__main__':
    rgb = AstraProRgb(1)
    rgb.cam_visualize()

