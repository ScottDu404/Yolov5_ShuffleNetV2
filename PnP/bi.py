from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from math import radians, sin, cos


def set_axes_equal(ax):
# 这一段是copy别人的。用处不是很大。
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def dh_matrix(alpha, a, d, theta):
# 传入四个DH参数，根据公式3-6，输出一个T矩阵。
    alpha = alpha / 180 * np.pi
    theta = theta / 180 * np.pi
    matrix = np.identity(4)
    matrix[0,0] = cos(theta)
    matrix[0,1] = -sin(theta)
    matrix[0,2] = 0
    matrix[0,3] = a
    matrix[1,0] = sin(theta)*cos(alpha)
    matrix[1,1] = cos(theta)*cos(alpha)
    matrix[1,2] = -sin(alpha)
    matrix[1,3] = -sin(alpha)*d
    matrix[2,0] = sin(theta)*sin(alpha)
    matrix[2,1] = cos(theta)*sin(alpha)
    matrix[2,2] = cos(alpha)
    matrix[2,3] = cos(alpha)*d
    matrix[3,0] = 0
    matrix[3,1] = 0
    matrix[3,2] = 0
    matrix[3,3] = 1
    return matrix

joint_num = 7

# --- Robotic Arm construction ---
# DH参数表，分别用一个列表来表示每个关节的东西。
joints_alpha = [0, 90, 90, 90, 90, 90, 90]
joints_a = [0, 0, 0, 0, 0, 0, 0]
joints_d = [0.31, 0.0, 0.4, 0.0, 0.4, 0.0, 0.175]
joints_theta = [0, 180, 180, 180, 180, 180, 180]

#    Joint Angle variables
# joints_angle = [-0.001, -21.0, -0.001, -21.0, 0.0, 0.0, -0.0]
# 选定几个特定的关节角，看看算出来的值，和真实值是否一致，方向是否反了。
joints_angle = [2, -23.43, 0, 50, 1, 0, 0]
#    DH参数转转换矩阵T---------------------
joint_hm = []
for i in range(joint_num):
    joint_hm.append(dh_matrix(joints_alpha[i], joints_a[i], joints_d[i], joints_theta[i]+joints_angle[i]))

# -----------连乘计算----------------------
for i in range(joint_num-1):
    joint_hm[i+1] = np.dot(joint_hm[i], joint_hm[i+1])
# Prepare the coordinates for plotting
for i in range(joint_num):
    print(np.round(joint_hm[i][:3, 3], 5))
# 获取坐标值
X = [hm[0, 3] for hm in joint_hm]
Y = [hm[1, 3] for hm in joint_hm]
Z = [hm[2, 3] for hm in joint_hm]
# Plot
ax = plt.axes(projection='3d')
# ax.set_aspect('equal')
ax.plot3D(X, Y, Z)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

set_axes_equal(ax)
plt.show()