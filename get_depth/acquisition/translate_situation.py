# -*- coding: utf-8 -*-
"""
@Time : 2022-09-30 21:23
@Auth : NopainMea
@File :translate_situation.py
@IDE :PyCharm
@E-mail : 3284346435@qq.com
"""
import os.path

import cv2

import acq_rgb
import acq_depth
import yaml
import numpy as np


class ImgDeal(object):
    def __init__(self, yml_path='../configs/astra_pro_calibration.yml'):
        super(ImgDeal, self).__init__()
        self.cv_file = cv2.FileStorage(yml_path, cv2.FILE_STORAGE_READ)
        self.K = self.cv_file.getNode("K").mat()
        self.D = self.cv_file.getNode("D").mat()
        self.img_size = tuple(self.cv_file.getNode("size").mat().reshape(-1).astype(np.int32))

    def dist_correct(self, input_img):
        w, h = self.img_size
        mapx, mapy = cv2.initUndistortRectifyMap(self.K, self.D, None, self.K, (w, h), 5)
        output_img = cv2.remap(input_img, mapx, mapy, cv2.INTER_LINEAR)
        return output_img

    def translate_to_camera_coordinate(self, depth, pixu, pixv):
        invK = np.linalg.inv(self.K)
        camera_cor = np.dot(invK, np.array([depth*pixu, depth*pixv, depth]))
        return camera_cor


if __name__ == '__main__':
    img_deal = ImgDeal()
    img = cv2.imread('img.png')
    new_img = img_deal.dist_correct(img)
    # cv2.imshow('data', new_img)
    # cv2.waitKey(0)
    print(img_deal.translate_to_camera_coordinate(100, 600, 400))
