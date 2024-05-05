import matplotlib.pyplot as plt
import seaborn as sns

# Default plot parameters
plt.rcParams['figure.figsize'] = (10, 6)  # Default figure size
plt.rcParams['font.size'] = 18  # Default font size
plt.rcParams['axes.titlesize'] = 24  # Default title font size
plt.rcParams['axes.labelsize'] = 18  # Default label font size
plt.rcParams['lines.linewidth'] = 4  # Default line width
plt.rcParams['axes.grid'] = True  # Show grid by default
plt.rcParams['xtick.labelsize'] = 14  # Default tick label font size
plt.rcParams['ytick.labelsize'] = 14  # Default tick label font size
plt.rcParams['legend.fontsize'] = 16  # Default legend font size

sns.set_palette("colorblind")  # You can change "viridis" to other palettes provided by Seaborn


ALPHA = 0.3
