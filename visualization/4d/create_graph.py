import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def plot_4d(df, x_col='r1', y_col='r2', z_col='r3', val_col='val', cmap='viridis', marker_size=50):
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

def main(filepath):
    """
    Main function to run the pipeline.
    
    Parameters:
        filepath (str): Path to the CSV file.
    """
    # Load data
    df = load_data(filepath)
    
    # Plot data
    plot_4d(df)

# Example usage
if __name__ == "__main__":
    filepath = './visualization/graphs/4d/test.csv'  # Replace with your actual file path
    main(filepath)
