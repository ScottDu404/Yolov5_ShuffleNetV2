import cv2
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageDraw
# https://cloud.tencent.com/developer/article/2092184
depth_f = [577.134, 577.134]  # ir相机的内参_fx,fy
depth_c = [322.31, 242.271]  # ir相机的内参_u0,v0
rgb_f = [514.656, 514.656]  # rgb相机的内参_fx,fy
rgb_c = [337.437, 239.921]  # rgb相机的内参_u0,v0

# RT矩阵

depth_rgb_r = np.array([[0.999903, -0.0129438, -0.00521312],
                        [0.0129686, 0.999905, 0.00474647],
                        [0.00515118, -0.00481362, 0.999975]])
depth_rgb_t = np.array([-25.3494, -0.151612, -0.159334])


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
            # print(z)
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
    print(world_coord.shape)
    print(R)
    print(t)
    cam_coord = np.dot(R, world_coord.transpose(1, 0)).transpose(1, 0) + t.reshape(1, 3)
    return cam_coord


def cam2pixel(cam_coord, num, f, c):
    # 实现相机坐标系到像素坐标系的转换
    # c,f:相机内参
    depth_zeros = np.zeros((480, 640))
    for i in range(num):

        u = (cam_coord[i][0]) / (cam_coord[i][2]) * f[0] + c[0]
        v = (cam_coord[i][1]) / (cam_coord[i][2]) * f[1] + c[1]
        z = cam_coord[i][2]
        if (0 <= u < 640) and (0 <= v < 480):
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

depth_path = '../img/depth00000001.png'
ir_path = '../img/rgb00000001.png'
# 这样才是读取深度图
oridepth = cv2.imread(depth_path, -1)
oriir = cv2.imread(ir_path)
print(oridepth)
# print(oridepth.shape)
depth_cam, num = depth_pixel2cam(oridepth, depth_c, depth_f)
depth2rgb_cam = depth2rgb(depth_cam, depth_rgb_r, depth_rgb_t)  # 获取rgb相机坐标系下的depth
#TODO：RGB和深度对齐了，深度转到了RGB像素上，接下来就是用苹果定位中心点的像素坐标转化成三维坐标了，需要的是RGB相机的参数
rgb_depth = cam2pixel(depth2rgb_cam, num, rgb_f, rgb_c)
depth_uint16 = rgb_depth.astype(np.uint16)
# 这里要把它转化为uint16才能保存为16位的深度图
cv2.imwrite("../img/depth00000001_s.png", rgb_depth.astype(np.uint16))
print(depth_cam.shape)
# cv2.imshow('555', oridepth)
cv2.imshow('depth', rgb_depth)

cv2.imshow('rgb', oriir)
cv2.waitKey(0)
# with open(kps, 'r') as file_obj:
#     json_data = json.load(file_obj)
#     kps_i = loadjson(json_data)  # 获取UV值
#     kps = kps_i
#
#     whole_kps = get_depth(kps, depth_uint16)  # 获取rgb的UVZ
#
#     # step4 rgb_kp2ir
# cam_rgb = pixel2cam(whole_kps, rgb_c, rgb_f)
#
# r = depth_rgb_r
# r_inv = np.linalg.inv(r)
#
# cam_ir = rgb2ir(cam_rgb, r_inv, depth_rgb_t)
# kp_ir = cam2pixel_2(cam_ir, depth_f, depth_c)



