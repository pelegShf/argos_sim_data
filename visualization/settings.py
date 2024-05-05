import matplotlib.pyplot as plt
import seaborn as sns

# Default plot parameters
plt.rcParams['figure.figsize'] = (10, 6)  # Default figure size
plt.rcParams['font.size'] = 12  # Default font size
plt.rcParams['axes.titlesize'] = 16  # Default title font size
plt.rcParams['axes.labelsize'] = 14  # Default label font size
plt.rcParams['lines.linewidth'] = 2  # Default line width
plt.rcParams['axes.grid'] = True  # Show grid by default
plt.rcParams['xtick.labelsize'] = 10  # Default tick label font size
plt.rcParams['ytick.labelsize'] = 10  # Default tick label font size
plt.rcParams['legend.fontsize'] = 12  # Default legend font size

sns.set_palette("colorblind")  # You can change "viridis" to other palettes provided by Seaborn


ALPHA = 0.3
