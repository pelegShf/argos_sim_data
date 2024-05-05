import time
import pandas as pd
import numpy as np


# Polarization metric

# def polarization(df):
#     N = len(df)
#     deadCount = df['IsFaulty'].sum()
#     sum = np.array([0.0, 0.0])
#     for _, row in df.iterrows():
#         thetha_i = row['Heading']
#         thetha_i = np.radians(thetha_i % 360)  # Convert to radians and normalize
#         currentHeadingVec = np.array([np.cos(thetha_i), np.sin(thetha_i)])  # Create a unit vector at the angle thetha_i
#         if not row['IsFaulty']:
#             sum += currentHeadingVec
    
#     sum /= (N - deadCount)
#     order = np.linalg.norm(sum)
#     return order

def polarization(df):
    N = len(df)

    # Convert to radians and normalize
    thetha_i = np.radians(df['Heading'] % 360)

    # Create a unit vector at the angle thetha_i
    currentHeadingVec = np.column_stack((np.cos(thetha_i), np.sin(thetha_i)))

    # Only consider rows where 'IsFaulty' is False
    currentHeadingVec = currentHeadingVec[df['IsFaulty'] == False]
    # Calculate the sum
    sum = currentHeadingVec.sum(axis=0)

    # Normalize the sum
    sum /= (N - df['IsFaulty'].sum())

    # Calculate the order
    order = np.linalg.norm(sum)

    return order

def get_order(df, num_rows_per_timestep):
    order_series = df.groupby('TimeStep').apply(polarization)
    order_series = order_series.round(4)
    # order_series = data_cleaning(order_series)

    return order_series

