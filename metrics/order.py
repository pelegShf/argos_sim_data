import time
import pandas as pd
import numpy as np

from consts import PRECISION, TIMESTEP_COL, IS_FAULTY_COL,HEADING_COL


# Polarization metric
def polarization(df):
    N = len(df)

    # Convert to radians and normalize
    thetha_i = np.radians(df[HEADING_COL] % 360)

    # Create a unit vector at the angle thetha_i
    currentHeadingVec = np.column_stack((np.cos(thetha_i), np.sin(thetha_i)))

    # Only consider rows where 'IsFaulty' is False if the column exists
    if(IS_FAULTY_COL in df.columns):
        print(df[IS_FAULTY_COL])
        currentHeadingVec = currentHeadingVec[df[IS_FAULTY_COL] == False]
    # Calculate the sum
    sum = currentHeadingVec.sum(axis=0)

    # Normalize the sum
    if IS_FAULTY_COL in df.columns:
        sum /= (N - df[IS_FAULTY_COL].sum())
    else:
        sum /= N

    # Calculate the order
    order = np.linalg.norm(sum)

    return order

def get_order(df, num_rows_per_timestep):
    order_series = df.groupby(TIMESTEP_COL).apply(polarization)
    order_series = order_series.round(PRECISION)
    # order_series = data_cleaning(order_series)

    return order_series

