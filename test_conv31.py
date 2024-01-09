import torch
import torch.nn as nn


def depthwise_conv(i, o, kernel_size, stride=1, padding=0, bias=False):
    return nn.Conv2d(i, o, kernel_size, stride, padding, bias=bias, groups=i)

in_put = torch.randn(32, 5, 5)
print(in_put.shape)
c33 = nn.Conv2d(32, 32, (3, 3))
# c31 = nn.Conv2d(32, 32, (3, 1))
# c13 = nn.Conv2d(32, 32, (1, 3))
out_put = c33(in_put)
# out_put1 = c13(c31(in_put))
# print(out_put.shape)
# print(out_put1.shape)

# depc33 = depthwise_conv(32, 32, kernel_size=3, stride=1, padding=1)
# print(depc33(in_put).shape)
# depc13 = nn.Conv2d(32, 32, kernel_size=(1, 3), stride=1, padding=(0, 1))
# print(depc13(in_put).shape)
# depc31 = depthwise_conv(32, 32, kernel_size=(3, 1), stride=1, padding=(1, 0))
# print(depc31(depc13(in_put)).shape)
#
# b33 = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1, bias=False),
# b13 = nn.Conv2d(32, 32, kernel_size=(1, 3), stride=2, padding=(0, 1), bias=False),
# b31 = nn.Conv2d(32, 32, kernel_size=(3, 1), stride=2, padding=(1, 0), bias=False),


IN = torch.tensor([
            [[1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0]],
            [[1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0]],
            [[1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0]]
            ])
print(IN.shape)

# fliter = nn.Conv2d(3, 3, (3, 3), stride=1, padding=1)
fliter = depthwise_conv(3, 3, kernel_size=3, stride=2, padding=1)
fliter_31 = depthwise_conv(3, 3, kernel_size=(3, 1), stride=(2, 1), padding=(1, 0))
fliter_13 = depthwise_conv(3, 3, kernel_size=(1, 3), stride=(1, 2), padding=(0, 1))
OUT = fliter(IN)
OUT_31 = fliter_31(IN)
OUT_13 = fliter_13(OUT_31)
print(OUT)
print(OUT_13)






