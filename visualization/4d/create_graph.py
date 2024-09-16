import argparse
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def load_data(filepath):
    """
    Load data from a CSV file.
    
    Parameters:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the data.
    """
    df = pd.read_csv(filepath)
    return df




def plot_4d(df, x_col='r1', y_col='r2', z_col='r3', val_col='val', cmap='inferno', marker_size=50):
    """
    Plot a 4D scatter plot where color represents the fourth dimension.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_col (str): Column name for the x-axis (default: 'r1').
        y_col (str): Column name for the y-axis (default: 'r2').
        z_col (str): Column name for the z-axis (default: 'r3').
        val_col (str): Column name for the values used in colormap (default: 'val').
        cmap (str): Colormap to use (default: 'viridis').
        marker_size (int): Size of the scatter markers (default: 50).
    """
    r1 = df[x_col]
    r2 = df[y_col]
    r3 = df[z_col]
    val = df[val_col]

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot points with color based on val
    sc = ax.scatter(r1, r2, r3, c=val, cmap=cmap, s=marker_size)

    # Add color bar which maps values to colors
    cbar = plt.colorbar(sc)
    cbar.set_label(val_col)

    # Labels
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)

    # Show plot
    plt.show()



def plot_2d_plane_in_3d(df,x_col='r1', y_col='r2', z_col='r3', val_col='val',mesh=False):
    r1 = df[x_col]
    r2 = df[y_col]
    r3 = df[z_col]
    val = df[val_col]

    # Convert the pandas Series to NumPy arrays
    r1 = df[x_col].to_numpy()
    r2 = df[y_col].to_numpy()
    r3 = df[z_col].to_numpy()
    val = df[val_col].to_numpy()

    # Ensure that r1, r2, r3, and val are reshaped into 2D arrays
    r1 = r1.reshape((int(np.sqrt(r1.size)), -1))
    r2 = r2.reshape((int(np.sqrt(r2.size)), -1))
    r3 = r3.reshape((int(np.sqrt(r3.size)), -1))
    val = val.reshape((int(np.sqrt(val.size)), -1))

    # Sample val data associated with each (r1, r2, r3) combination

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if mesh:
        # ax.plot_trisurf(r1, r2, r3, cmap='viridis', edgecolor='none')
        ax.plot_surface(r1, r2, r3, facecolors=plt.cm.viridis(val), shade=False, rstride=1, cstride=1)

    else:
        ax.scatter(r1, r2, r3, c=val, cmap='viridis',depthshade=False)

    # Plot the surface where color represents the value of 'val'
    ax.set_xlabel('r1')
    ax.set_ylabel('r2')
    ax.set_zlabel('r3')

    # Add color bar for reference
    mappable = plt.cm.ScalarMappable(cmap='viridis')
    mappable.set_array(val)
    plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)

    plt.show()

def plot_2d_plane_xy(df,fname=None):
    x_col='r1'
    y_col='r2'
    z_col='r3'
    val_col='val'
    r1 = df[x_col]
    r2 = df[y_col]
    r3 = df[z_col]
    val = df[val_col]

    mask = r2 < 0
    r1[mask] = np.nan
    r3[mask] = np.nan

    plt.figure()
    plt.scatter(r1, r3, c=val, cmap='viridis')

    plt.xlabel('r1')
    plt.ylabel('r3')
    plt.title('Mixed group - 55')

    # Add color bar for reference
    plt.colorbar(label='val')
    # Save the plot
    if fname:
        plt.savefig(fname)
    plt.show()

def plot_radar(df, x_col='r1', y_col='r2', z_col='r3', val_col='val'):
    r1 = df[x_col]
    r2 = df[y_col]
    r3 = df[z_col]
    val = df[val_col]

    # Number of variables
    num_vars = 3

    # Compute angle of each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Append the first value to close the radar chart
    r1 = np.append(r1, r1[0])
    r2 = np.append(r2, r2[0])
    r3 = np.append(r3, r3[0])
    angles += angles[:1]

    # Create radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw one axe per variable + add labels
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([x_col, y_col, z_col])

    # Plot the dots with color mapping
    cmap = plt.get_cmap('viridis')
    norm = Normalize(vmin=min(val), vmax=max(val))
    colors = cmap(norm(val))

    for i in range(len(val)):
        values = [r1[i], r2[i], r3[i]]
        ax.scatter(angles[:-1], values, c=[colors[i]], s=100, edgecolor='black')

    # Add a color bar for reference
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, label=val_col)

    plt.show()
def plot_3d_surface_with_values(df,x_col='r1', y_col='r2', z_col='r3', val_col='val',mesh=False):
    r1 = df[x_col]
    r2 = df[y_col]
    r3 = df[z_col]
    val = df[val_col]

    # Convert the pandas Series to NumPy arrays
    r1 = df[x_col].to_numpy()
    r2 = df[y_col].to_numpy()
    r3 = df[z_col].to_numpy()
    val = df[val_col].to_numpy()
    val = np.log(val + 1)

    # Ensure that r1, r2, r3, and val are reshaped into 2D arrays
    # r1 = r1.reshape((int(np.sqrt(r1.size)), -1))
    # r2 = r2.reshape((int(np.sqrt(r2.size)), -1))
    # r3 = r3.reshape((int(np.sqrt(r3.size)), -1))
    # val = val.reshape((int(np.sqrt(val.size)), -1))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if mesh:
        # ax.plot_trisurf(r1, r3, val, cmap='viridis', edgecolor='none')
        ax.plot_surface(r1, r3, val, cmap='viridis')
    else:
        ax.scatter(r1, r3, val, c=val, cmap='viridis',depthshade=False)

    ax.set_xlabel('r1')
    ax.set_ylabel('r3')
    ax.set_zlabel('val')

    plt.show()


def main(filepath,fname):
    """
    Main function to run the pipeline.
    
    Parameters:
        filepath (str): Path to the CSV file.
    """
    # Load data
    df = load_data(filepath)
    
    # plot_2d_plane_in_3d(df)
    plot_2d_plane_xy(df,fname)
    # plot_radar(df)
    # plot_3d_surface_with_values(df)
    # Plot data
    # plot_4d(df)

# Example usage
if __name__ == "__main__":
    INPUT_FOLDER = "./visualization/graphs/4d/"
    CSV_FILE = ".csv"
    # Get the filepath from the command line using args
    parser = argparse.ArgumentParser(description="Process experiment data and create a CSV for plotting.")
    parser.add_argument('-i', type=str, help="File name containing results (without .csv)")

    args = parser.parse_args()

    

    main(INPUT_FOLDER + args.i+CSV_FILE,fname=f"{args.i}.jpg")
    
    
    # filepath = './visualization/graphs/4d/40_mix.csv'  # Replace with your actual file path
    # main(filepath)
