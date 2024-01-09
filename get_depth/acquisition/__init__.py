# -*- coding: utf-8 -*-
"""
@Time : 2022-09-03 10:41
@Auth : NopainMea
@File :__init__.py.py
@IDE :PyCharm
@E-mail : 3284346435@qq.com
"""


class BaseAcquisition(object):
    def __init__(self):
        self.height = None
        self.width = None
        self.fps = None
        pass

    def acq_image(self, *args, **kwargs):
        pass

    def calibrate(self, *args, **kwargs):
        pass

    def img_reshape(self, shape):
        pass

    def cam_visualize(self, *args, **kwargs):
        pass
