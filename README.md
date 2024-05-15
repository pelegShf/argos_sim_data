# Argos Simulation Data Library

This library provides tools for generating, manipulating, and visualizing simulation data for the Argos project.

## Features

- Generate random series of data for testing and development.
- Save series data to CSV files.
- Calculate various metrics for series data.
- Plot series of data with various options for customization.

## How to Use

### Command Line Arguments

You can customize the behavior of the script using the following command line arguments:

- `-i` or `--input_path`: This argument specifies the template for experiments. It should be a string representing the path to the input file. If not provided, it defaults to an empty string.

- `-d` or `--debug`: This argument enables or disables debug mode. It should be an integer where 0 means false (debug mode off) and 1 means true (debug mode on). If not provided, it defaults to 0 (off).

- `-m` or `--metric`: This argument specifies the metrics to be used. It should be a comma-separated list of metrics. Available metrics are: "order", "union", "centers", "avg_distance", "speed". If "all" is provided or if this argument is not provided, all metrics will be used.

- `-l` or `--log`: This argument enables or disables logging. It should be an integer where 0 means false (logging off) and 1 means true (logging on). If not provided, it defaults to 1 (on).

Here's an example of how to run the script with command line arguments:

```bash
python main.py -i "/path/to/input" -d 1 -m "order,avg_distance" -l 0
```

### Generating and Saving Data

1. Clone this repository to your local machine.
2. Navigate to the directory containing the library files.
3. Import the necessary functions from the library in your Python script.
4. Generate series data and save it to a CSV file.

Example usage:

```python
from argos_sim_data import generate_series, save_to_csv
import numpy as np

num_series = 10
series_list = [np.random.rand(100) for _ in range(num_series)]  # Generate random series for demonstration
save_to_csv(series_list, 'series_data.csv')

This will generate a list of random series and save it to a CSV file named 'series_data.csv'.

```

## Calculating Metrics

To calculate metrics for your series data, use the calculate_metrics function. This function will return a dictionary containing the mean, median, standard deviation, and variance for each series.

Example usage:

```python
from argos_sim_data import calculate_metrics

metrics = calculate_metrics(series_list)
print(metrics)
```


This will print out the calculated metrics for each series in series_list.


## Plotting Data
To plot your series data, use the plot_series function.

Example usage:
```python
from argos_sim_data import plot_series

plot_series(series_list, avg=True, show_individual=False, error_type='se', to_pdf=True)
```
This will plot the series data using the settings defined in settings_to_print.py.

