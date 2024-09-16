import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_2d_plane_in_3d(df):
   r1 = np.arange(0, 1.1, 0.1)
   r3 = np.arange(0, 1.1, 0.1)
   r1, r3 = np.meshgrid(r1, r3)
   r2 = 1 - (r1 + r3)
   
   
   mask = r2 < 0
   r1[mask] = np.nan
   r2[mask] = np.nan
   r3[mask] = np.nan
   
   # Sample val data associated with each (r1, r2, r3) combination
   val = np.sin(r1) + np.cos(r3)  # Example data
   
   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
   
   # Plot the surface where color represents the value of 'val'
   ax.plot_surface(r1, r2, r3, facecolors=plt.cm.viridis(val), shade=False, rstride=1, cstride=1)
   
   ax.set_xlabel('r1')
   ax.set_ylabel('r2')
   ax.set_zlabel('r3')
   
   # Add color bar for reference
   mappable = plt.cm.ScalarMappable(cmap='viridis')
   mappable.set_array(val)
   plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)
   
   plt.show()


def plot_2d_plane_xy():
   r1 = np.arange(0, 1.1, 0.1)
   r3 = np.arange(0, 1.1, 0.1)
   r1, r3 = np.meshgrid(r1, r3)
   r2 = 1 - (r1 + r3)
   
   mask = r2 < 0
   r1[mask] = np.nan
   r3[mask] = np.nan
   
   # Sample val data associated with each (r1, r2, r3) combination
   val = np.sin(r1) + np.cos(r3)  # Example data
   
   plt.figure()
   plt.scatter(r1, r3, c=val, cmap='viridis')
   
   plt.xlabel('r1')
   plt.ylabel('r3')
   plt.title('2D Plane Projection onto XY Plane')
   
   # Add color bar for reference
   plt.colorbar(label='val')
   
   plt.show()


def plot_3d_surface_with_values(df):
   r1 = np.arange(0, 1.1, 0.1)
   r3 = np.arange(0, 1.1, 0.1)
   r1, r3 = np.meshgrid(r1, r3)
   r2 = 1 - (r1 + r3)
   
   mask = r2 < 0
   r1[mask] = np.nan
   r2[mask] = np.nan
   r3[mask] = np.nan
   
   # Replace this with your actual value calculation
   val = np.sin(r1) + np.cos(r3)
   
   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
   
   ax.plot_surface(r1, r3, val, cmap='viridis')
   
   ax.set_xlabel('r1')
   ax.set_ylabel('r3')
   ax.set_zlabel('val')
   
   plt.show()



# Call this function to see the 2D plane in 3D
plot_2d_plane_in_3d()

# Call this function to see the 2D plane projected onto the XY plane
plot_2d_plane_xy()

# Call this function to see the final 3D plot with values on the z-axis
plot_3d_surface_with_values()
