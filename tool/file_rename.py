import os
import tqdm
# filepath = '../../datasets/VOC2007/images/'
# filepath = '../../datasets/VOC2007/labels/'
filepath = 'D:/Procedure/python/yolov5/datasets/total_data/images/'
# filepath = 'D:/Procedure/python/yolov5/datasets/apple_data 2.0/background/images/'
filename = open("djcoco.txt").read().split('\n')
print(filename)


for i, index in enumerate(filename):
    # print(filepath + 'images/' + str(i).rjust(5, '0') + '.jpg')
    # print(filepath + index + '.png')
    try:
        # os.rename(filepath + index + '.txt', filepath + str(i).rjust(5, '0') + '.jpg')
        os.rename(filepath + index + '.jpg', filepath + str(i+9198).rjust(5, '0') + '.jpg')
    except FileNotFoundError:
        print(filepath + index + '.txt', filepath + str(i).rjust(5, '0') + '.txt')
        # os.rename(filepath + index + '.png', filepath + str(i).rjust(5, '0') + '.jpg')
