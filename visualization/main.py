import matplotlib.pyplot as plt

def plot_series(series_list, filename=None):
    for i, series in enumerate(series_list):
        plt.plot(series, label=f"Series {i+1}")
    plt.legend()
    if filename is not None:
        plt.savefig(f'{filename}.png')
    else:
        plt.show()
    plt.clf()