# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys

path1 = 'D:/Procedure/python/yolov5/datasets/total_data/labels'  # 所需修改文件夹所在路径
dirs = os.listdir(path1)

count = 0
for dir in dirs:
    new_path = 'D:/Procedure/python/yolov5/datasets/total_data/labels'
    n = 0
    for j in range(len(dirs)):
        old_path = path1 + os.sep + dir
        # 获取该目录下所有文件，存入列表中
        fileList = os.listdir(old_path)
        for i in fileList:
            # 设置旧文件名（就是路径+文件名）
            oldname = old_path + os.sep + i  # os.sep添加系统分隔符
            # print(oldname)

            # 设置新文件名
            newname = new_path + os.sep + str(count+4465).rjust(5, '0') + '.jpg'
            # print(newname)

            os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
            print(oldname, '======>', newname)

            n += 1
            count += 1
    print(dir+'重命名文件数:',n)
print('重命名文件总数：', count)
