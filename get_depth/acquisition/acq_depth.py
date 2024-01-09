# -*- coding: utf-8 -*-
"""
@Time : 2022-09-03 17:07
@Auth : NopainMea
@File :acq_depth.py
@IDE :PyCharm
@E-mail : 3284346435@qq.com
"""

from get_depth.acquisition import BaseAcquisition
from openni import openni2
import numpy as np
import cv2


class AcqDepth(BaseAcquisition):
    def __init__(self):
        super(AcqDepth, self).__init__()
        pass

    def acq_depth(self, *args, **kwargs):
        pass


class AstraProDph(AcqDepth):
    def __init__(self):
        super(AstraProDph, self).__init__()
        openni2.initialize()
        self.dev = openni2.Device.open_any()
        self.depth_stream = self.dev.create_depth_stream()
        self.depth_stream.start()
        self.frame = None
        self.dpt = None

    def acq_depth(self):
        self.frame = self.depth_stream.read_frame()
        dframe_data = np.array(self.frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        dpt2 *= 255
        self.dpt = (dpt1 + dpt2)
        return self.dpt

    def img_reshape(self, shape):
        depth = cv2.resize(self.dpt, shape)
        return depth

    def __mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(y, x, self.dpt[y, x])

    def cam_visualize(self, windows_name='depth'):
        cv2.namedWindow(windows_name)
        cv2.setMouseCallback(windows_name, self.__mouse_callback)
        while True:
            self.acq_depth()
            cv2.imshow(windows_name, self.dpt)
            cv2.waitKey(1)


if __name__ == '__main__':
    dep = AstraProDph()
    dep.cam_visualize()
    # while True:
    #     dep.acq_depth()
    #     dpt = dep.img_reshape((1920, 1080))
    #     cv2.imshow('depth', dpt)
    #     cv2.waitKey(1)


