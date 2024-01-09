# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ['apple']  # 改成自己的类别
abs_path = os.getcwd()
print(abs_path)


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open('D:/Procedure/python/yolov5/apple2/Annotations/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open('D:/Procedure/python/yolov5/apple2/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        if obj.find('difficult'):
            difficult = float(obj.find('difficult').text)
        else:
            difficult = 0
        # difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        # print(cls_id)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
for image_set in sets:
    # if not os.path.exists('D:/Procedure/python/labels/'):
    #     os.makedirs('D:/Procedure/python/labels/')
    image_ids = open('D:/Procedure/python/yolov5/yolov5-master/tool/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()

    if not os.path.exists('D:/Procedure/python/yolov5/yolov5-master/tool/dataSet_path/'):
        os.makedirs('D:/Procedure/python/yolov5/yolov5-master/tool/dataSet_path/')

    list_file = open('D:/Procedure/python/yolov5/yolov5-master/tool/dataSet_path/%s.txt' % (image_set), 'w')
    # 这行路径不需更改，这是相对路径
    for image_id in image_ids:
        list_file.write('D:/Procedure/python/yolov5/apple2/JPEGImages/JPEGImages/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()

