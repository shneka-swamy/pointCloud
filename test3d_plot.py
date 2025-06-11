import matplotlib.pyplot as plt
import numpy as np

# prepare some coordinates
x, y, z = np.indices((5, 8, 6))

# draw cuboids in the top left and bottom right corners, and a link between
# them
cube1 = (x < 3) & (y < 3) & (z < 3)
cube2 = (x >= 5) & (y >= 5) & (z >= 5)
link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

# combine the objects into a single boolean array
voxelarray = cube1 | cube2 | link
print("Voxel array is: ", voxelarray)

# set the colors of each object
colors = np.zeros((5, 8, 6, 3), dtype=int)
colors[link] = [255,0,0]
colors[cube1] = [0,255,0]
colors[cube2] = [0,0, 255]

colors = colors.astype(float) / 255.0

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

plt.show()