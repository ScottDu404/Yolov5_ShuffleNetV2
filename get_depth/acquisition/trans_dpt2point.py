import cv2
import numpy as np
import open3d as o3d

import time

# https://blog.csdn.net/FUTEROX/article/details/126128581

class point_cloud_generator():

    def __init__(self, rgb_file, depth_file, save_ply, camera_intrinsics):
        self.rgb_file = rgb_file
        self.depth_file = depth_file
        self.save_ply = save_ply

        self.rgb = cv2.imread(rgb_file)
        self.depth = cv2.imread(self.depth_file, -1)

        print("your depth image shape is:", self.depth.shape)

        self.width = self.rgb.shape[1]
        self.height = self.rgb.shape[0]

        self.camera_intrinsics = camera_intrinsics
        self.depth_scale = 1000

        self.point = (0, 0, 0)

    def compute(self):
        t1 = time.time()
        depth = np.asarray(self.depth, dtype=np.uint16).T
        # depth[depth==65535]=0
        self.Z = depth / self.depth_scale
        fx, fy, cx, cy = self.camera_intrinsics

        X = np.zeros((self.width, self.height))
        Y = np.zeros((self.width, self.height))
        for i in range(self.width):
            X[i, :] = np.full(X.shape[1], i)

        self.X = ((X - cx ) * self.Z) / fx
        for i in range(self.height):
            Y[:, i] = np.full(Y.shape[0], i)
        self.Y = ((Y - cy ) * self.Z) / fy

        data_ply = np.zeros((6, self.width * self.height))
        data_ply[0] = self.X.T.reshape(-1)
        data_ply[1] = -self.Y.T.reshape(-1)
        data_ply[2] = -self.Z.T.reshape(-1)
        img = np.array(self.rgb, dtype=np.uint8)
        data_ply[3] = img[:, :, 0:1].reshape(-1)
        data_ply[4] = img[:, :, 1:2].reshape(-1)
        data_ply[5] = img[:, :, 2:3].reshape(-1)
        self.data_ply = data_ply
        t2 = time.time()
        print('calcualte 3d point cloud Done.', t2 - t1)


    def compute_uv(self, u, v, r):
        depth = np.asarray(self.depth, dtype=np.uint16).T
        # depth[depth==65535]=0
        self.Z = depth / self.depth_scale
        fx, fy, cx, cy = self.camera_intrinsics
        self.Z_mean = float(np.mean(self.Z[u-r:u+r, v-r:v+r]))
        # print(self.Z[u][v], z_mean)
        self.x = ((u - cx) * self.Z_mean) / fx
        self.y = ((v - cy) * self.Z_mean) / fy
        self.point = (round(self.x, 3), round(self.y, 3), round(self.Z_mean, 3))
        return self.point



    def write_ply(self):
        start = time.time()
        float_formatter = lambda x: "%.4f" % x
        points = []
        for i in self.data_ply.T:
            points.append("{} {} {} {} {} {} 0\n".format
                          (float_formatter(i[0]), float_formatter(i[1]), float_formatter(i[2]),
                           int(i[3]), int(i[4]), int(i[5])))

        file = open(self.save_ply, "w")
        file.write('''ply
        format ascii 1.0
        element vertex %d
        property float x
        property float y
        property float z
        property uchar red
        property uchar green
        property uchar blue
        property uchar alpha
        end_header
        %s
        ''' % (len(points), "".join(points)))
        file.close()

        end = time.time()
        print("Write into .ply file Done.", end - start)

    def show_point_cloud(self):
        pcd = o3d.io.read_point_cloud(self.save_ply)
        o3d.visualization.draw_geometries([pcd], point_show_normal=True, width=800, height=600)


if __name__ == '__main__':
    # 代码测试
    # 上面的是IR摄像头的参数，下面的是RGB摄像头的参数，之前测得不准是因为用的IR参数，而IR的图早已经对齐到RGB图上了，所以应该用RGB相机的参数才对
    # camera_intrinsics = [577.134, 577.134, 322.31, 242.271]
    camera_intrinsics = [514.656, 514.656, 337.437, 239.921]
    rgb_file = "../img/img.png"
    depth_file = "../img/depth00000001_s.png"
    save_ply = "data.ply"
    a = point_cloud_generator(rgb_file=rgb_file,
                              depth_file=depth_file,
                              save_ply=save_ply,
                              camera_intrinsics=camera_intrinsics
                              )
    # a.compute()
    # point = a.compute_uv(289, 289, 3)
    # point = a.compute_uv(217, 202, 3)
    point = a.compute_uv(339, 168, 3)
    print("苹果位置：{}m,{}m,{}m".format(point[0], point[1], point[2]))
    # a.write_ply()
    # a.show_point_cloud()



