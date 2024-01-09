import open3d as o3d
# import open3d_tutorial as o3dtut
import numpy as np

print("Open3D read Point Cloud")
pcd = o3d.io.read_point_cloud("data.ply")
# pcd = o3d.io.read_triangle_mesh("data/bun315.ply")  # newrabbit.pcd")
# print(pcd)
o3d.visualization.draw_geometries([pcd], point_show_normal=True, width=800, height=600)
print(pcd)
dumppcd = pcd.voxel_down_sample(voxel_size=0.001)  # 下采样（降采样）

dumppcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=30))
# 修改法线方向，为z轴，效果好了一点。。。而已
o3d.geometry.PointCloud.orient_normals_to_align_with_direction(dumppcd, orientation_reference=np.array([0.0, 0.0, 1.0]))
# o3d.geometry.PointCloud.orient_normals_towards_camera_location(dumppcd, camera_location=np.array([0., 0., 0.]))  #让法向量的方向都指向给定的相机位置
#-o3d.visualization.draw_geometries([dumppcd], point_show_normal=True)

print(dumppcd.normals[0])
dumppcd.orient_normals_consistent_tangent_plane(10)  # 最小生成树
print(np.asarray(pcd.normals)[:10, :])  # 输出前10个点的法向量
o3d.visualization.draw_geometries([dumppcd], point_show_normal=True, window_name="open",
                                  width=1024, height=768,
                                  left=50, top=50,
                                  mesh_show_back_face=False)  # 可视化点云和法线

radii=[0.005, 0.01, 0.02, 0.04]
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd=dumppcd, depth=8, width=0, scale=1.1)[0]
o3d.visualization.draw_geometries([dumppcd, poisson_mesh], width=1280, height=720)
#ball_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(dumppcd, o3d.utility.DoubleVector(radii))
#o3d.visualization.draw_geometries([ball_mesh], point_show_normal=True)
#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha=2)
o3d.visualization.draw_geometries([poisson_mesh])
#rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(dumppcd, o3d.utility.DoubleVector(radii))
#o3d.visualization.draw_geometries([dumppcd, rec_mesh], width=1280, height=720)
o3d.io.write_triangle_mesh("bun3.obj", poisson_mesh, write_ascii=True)
