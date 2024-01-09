#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys

# path = "../../datasets/VOC2007/images"
path = 'D:/Procedure/python/yolov5/datasets/9198+525苹果目标检测数据集（yolo格式）/test/images'
myList = os.listdir(path)

with open("D:/Procedure/python/yolov5/datasets/9198+525苹果目标检测数据集（yolo格式）/test/test.txt", 'a', encoding='utf-8') as filetext:
	for root,dirs,files in os.walk(path):
		for name in files:
			# print(name)
			# filetext.write(name[:-4]+"\n")
			filetext.write(path+'/' + name + "\n")
		for name in dirs:
			print(os.path.join(root,name))
			filetext.write(os.path.join(root,name)+"\n\n")

filetext.close()