import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_dir = "../data/DB/09062024_1459/avoidAttract/40/hyperparameter_set_0/X_RAY/closest_count_3.csv"
df = pd.read_csv(file_dir)

# Plot the histogram
plt.bar(df['VectorSize'], df['Count'])
plt.xlabel('Vector Size')
plt.ylabel('Count')
plt.title('Histogram of Vector Sizes')
plt.show()