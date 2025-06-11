import argparse
import pyvista as pv
import numpy as np
import glob
import matplotlib.pyplot as plt
from tqdm import tqdm

def argparser():
    parser = argparse.ArgumentParser("Converting point cloud to voxelization -- own function")
    parser.add_argument('--input_directory', help="Path to the input directory",  default='./soldier/soldier/Ply/')
    parser.add_argument('--verbose', help="verbose mode -- prints a lot of details", action='store_true')
    parser.add_argument('--width', help="Width of the cube considered for voxelization", default=10, type=int)
    return parser.parse_args()

def deter_no_voxels(args, pcd, width):
    x = pcd.points[:, 0]
    y = pcd.points[:, 1]
    z = pcd.points[:, 2]
    
    min_x = np.min(x)
    min_y = np.min(y)
    min_z = np.min(z)

    max_x = np.max(x)
    max_y = np.max(y)
    max_z = np.max(z)

    count_x = int((max_x - min_x) // width)
    count_y = int((max_y - min_y) // width)
    count_z = int((max_z - min_z) // width)

    if args.verbose:
        print(f"X coordinate, maximum is {max_x} and minimum is {min_x}")
        print(f"Y coordinate, maximum is {max_y} and minimum is {min_y}")
        print(f"Z coordinate, maximum is {max_z} and minimum is {min_z}")

    return {'x': count_x + 1, 'y': count_y + 1 , 'z': count_z + 1}, [min_x, min_y, min_z]

def voxelize(args, pcd, width):
        voxels, minimum = deter_no_voxels(args, pcd, width)
        count_points = np.zeros((voxels['x'], voxels['y'], voxels['z']), dtype=int)
        colors = np.zeros((voxels['x'], voxels['y'], voxels['z'], 3), dtype=int)
        lowest = np.zeros((voxels['x'], voxels['y'], voxels['z']), dtype=int)

        for i in tqdm(range(len(pcd.points))):
            point = pcd.points[i]
            color = pcd.point_data['RGB'][i]
            x_dim, y_dim, z_dim = (point - minimum) // width
            assert x_dim >= 0 and x_dim < voxels['x'], f"Error in x dimension calculation x_dim: {z_dim}, point0: {point[0]}"
            assert y_dim >= 0 and y_dim < voxels['y'], f"Error in y dimension calculation y_dim: {z_dim}, point1: {point[1]}"
            assert z_dim >= 0 and z_dim < voxels['z'], f"Error in z dimension calculation z_dim: {z_dim}, point2: {point[2]}"

            x_middle, y_middle, z_middle = (np.array([x_dim, y_dim, z_dim]) + minimum) * width + width // 2
            distance = np.linalg.norm(np.array([x_middle, y_middle, z_middle]) - point)
            if lowest[int(x_dim), int(y_dim), int(z_dim)] == 0 or lowest[int(x_dim), int(y_dim), int(z_dim)] > distance:
                colors[int(x_dim), int(y_dim), int(z_dim)] = color
                lowest[int(x_dim), int(y_dim), int(z_dim)] = distance
                
            count_points[int(x_dim), int(y_dim), int(z_dim)] += 1

        voxelarray = count_points > 0
        colors = colors.astype(float) / 255.0

        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        plt.show()

# NOTE: Here pyvista is used to only read the point cloud data
def read_point_cloud(args, file):
    pcd = pv.read(file) 
    if args.verbose:
        print(pcd)
        print("Length of the point cloud data is: ", len(pcd.points))
        print("Type of the read points is: ", type(pcd.points))
        print(pcd.point_data['RGB'])
    return pcd

def main():
    args = argparser()
    files = glob.glob(args.input_directory + '/*.ply')
    
    for file in files:
        pcd = read_point_cloud(args, file)
        voxelize(args, pcd, args.width)
        break

if __name__ == '__main__':
    main()