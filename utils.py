import pandas as pd
import numpy as np


def read_csv(file_path):
    return pd.read_csv(file_path)

# Pretty print the dataframe
def print_df(df):
    print(df)