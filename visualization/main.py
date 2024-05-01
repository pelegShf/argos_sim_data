import matplotlib.pyplot as plt
import numpy as np

def plot_series(series_list, filename=None,avg=True):
    avg_series = np.mean(series_list, axis=0)

    for i, series in enumerate(series_list):
        # plt.plot(series)
        plt.plot(series, label=f"Series {i+1}")
    # plt.legend()
    if avg:
        plt.plot(avg_series, color='black', label='Average Series')
    if filename is not None:
        plt.savefig(f'{filename}.png')
    else:
        plt.show()
        
    plt.clf()