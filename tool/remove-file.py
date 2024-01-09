import shutil
import os


file_new_path = 'D:/Procedure/python/yolov5/datasets/apple_data 2.0/train/labels/'
filename = open("D:/Procedure/python/yolov5/datasets/apple_data 2.0/train.txt").read().split('\n')
# print(filename)

for src in filename:
    src = src.replace('images', 'labels')
    src = src[:-4] + '.txt'
    # print(src)
    # name = src.split('\\')[-1]
    # print(name)
    # dst = file_new_path + name
    try:
        shutil.move(src, file_new_path)
    except FileNotFoundError:
        print(file_new_path)
