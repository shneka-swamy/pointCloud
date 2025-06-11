import open3d as o3d
import argparse
import glob
import time
import numpy as np
import trimesh

def argparser():
    parser = argparse.ArgumentParser("Generate voxelized image from point cloud")
    parser.add_argument('--input_directory', help="Path to the input directory", default='./soldier/soldier/Ply/')
    return parser.parse_args()

def convert_to_mesh(file):
    pcd = o3d.io.read_point_cloud(file)
    pcd.estimate_normals()


    # estimate radius for rolling ball
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 1.5 * avg_dist   

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pcd,
            o3d.utility.DoubleVector([radius, radius * 2]))

    # create the triangular mesh with the vertices and faces from open3d
    tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
                            vertex_normals=np.asarray(mesh.vertex_normals))

    trimesh.convex.is_convex(tri_mesh)

    # Convert trimesh to a format that is visualizable 
    # TODO: This part is not working -- can try rendering
    o3d_mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(np.asarray(tri_mesh.vertices)),
        o3d.utility.Vector3iVector(np.asarray(tri_mesh.faces))
        )

    if tri_mesh.vertex_normals is not None:
        o3d_mesh.vertex_normals = o3d.utility.Vector3dVector(np.asarray(tri_mesh.vertex_normals))

    o3d.visualization.draw_geometries([tri_mesh])

def voxelize(file, voxel_size):
    pcd = o3d.io.read_point_cloud(file)

    pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()),
            center=pcd.get_center())

    print('voxelization')
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,
                                                            voxel_size=voxel_size)

    o3d.visualization.draw_geometries([voxel_grid])

def main():
    args = argparser()
    files = glob.glob(args.input_directory + '/*.ply')
    count = 0

    for file in files:
        if count == 0:
            #convert_to_mesh(file)
            voxelize(file, 0.05)
        elif count == 1:
            voxelize(file, 0.005)
        elif count == 2:
            voxelize(file, 0.0005)
        else:
            break    

        count += 1


if __name__ == '__main__':
    main()