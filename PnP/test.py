import cv2
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageDraw

depth_f = [492.901337, 492.602295]  # ir相机的内参_fx,fy
depth_c = [317.839783, 273.10556]  # ir相机的内参_u0,v0
rgb_f = [823.490845, 822.888733]  # rgb相机的内参_fx,fy
rgb_c = [641.306152, 461.077454]  # rgb相机的内参_u0,v0
# RT矩阵
depth_rgb_r = np.array([[0.999890447, 0.00268923747, 0.0145565625]
                           , [-0.00259461207, 0.999975383, -0.00651552388]
                           , [-0.0145737259, 0.00647704117, 0.999872804]])
depth_rgb_t = np.array([19.7443695, -0.172736689, 0.248689786])


def depth_pixel2cam(depth, c, f):
    # 实现像素坐标系下的深度图转为相机坐标系
    # depth：深度图
    # c,f:depth相机的内参
    height = depth.shape[0]
    width = depth.shape[1]
    cam_coord = np.zeros((height * width, 3))
    num = 0
    for v in range(height):  # 480
        for u in range(width):  # 640
            z = depth[v][u]
            if z > 0:
                cam_coord[num][0] = (u - c[0]) * z / f[0]
                cam_coord[num][1] = (v - c[1]) * z / f[1]
                cam_coord[num][2] = z
                num += 1
            else:
                continue
    return cam_coord, num


def depth2rgb(world_coord, R, t):
    # 实现深度相机坐标系到RGB相机坐标系的转换
    # world_coord:depth相机坐标系下的深度图
    # R,T：depth→rgb的旋转平移矩阵
    cam_coord = np.dot(R, world_coord.transpose(1, 0)).transpose(1, 0) + t.reshape(1, 3)
    return cam_coord


def cam2pixel(cam_coord, num, f, c):
    # 实现相机坐标系到像素坐标系的转换
    # c,f:相机内参
    depth_zeros = np.zeros((960, 1280))
    for i in range(num):

        u = (cam_coord[i][0]) / (cam_coord[i][2]) * f[0] + c[0]
        v = (cam_coord[i][1]) / (cam_coord[i][2]) * f[1] + c[1]
        z = cam_coord[i][2]
        if (0 <= u < 1280) and (0 <= v < 960):
            depth_zeros[int(v)][int(u)] = z
    return depth_zeros


def pixel2cam(coords, c, f):
    cam_coord = np.zeros((len(coords), 3))
    z = coords[..., 2].reshape(-1, 1)

    cam_coord[..., :2] = (coords[..., :2] - c) * z / f
    cam_coord[..., 2] = coords[..., 2]

    return cam_coord


def cam2pixel_2(cam_coord, f, c):
    x = cam_coord[:, 0] / (cam_coord[:, 2]) * f[0] + c[0]
    y = cam_coord[:, 1] / (cam_coord[:, 2]) * f[1] + c[1]
    z = cam_coord[:, 2]
    img_coord = np.concatenate((x[:, None], y[:, None], z[:, None]), 1)
    return img_coord


def rgb2ir(world_coord, R, t):
    cam_coord = np.dot(R, (world_coord - t).transpose(1, 0)).transpose(1, 0)
    return cam_coord


oridepth = cv2.imread(depth_path, -1)
oriir = cv2.imread(ir_path)

depth_cam, num = depth_pixel2cam(oridepth, depth_c, depth_f)

depth2rgb_cam = depth2rgb(depth_cam, depth_rgb_r, depth_rgb_t)  # 获取rgb相机坐标系下的depth
rgb_depth = cam2pixel(depth2rgb_cam, num, rgb_f, rgb_c)
depth_uint16 = rgb_depth.astype(np.uint16)

with open(kps, 'r') as file_obj:
    json_data = json.load(file_obj)
    kps_i = loadjson(json_data)  # 获取UV值
    kps = kps_i

    whole_kps = get_depth(kps, depth_uint16)  # 获取rgb的UVZ

    # step4 rgb_kp2ir
cam_rgb = pixel2cam(whole_kps, rgb_c, rgb_f)

r = depth_rgb_r
r_inv = np.linalg.inv(r)

cam_ir = rgb2ir(cam_rgb, r_inv, depth_rgb_t)
kp_ir = cam2pixel_2(cam_ir, depth_f, depth_c)



