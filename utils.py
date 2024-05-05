import os
import pandas as pd
import numpy as np
import networkx as nx
from multiprocessing.shared_memory import SharedMemory

from visualization.main import plot_series
from consts import *


def read_csv(file_path):
    return pd.read_csv(file_path)

# def data_cleaning(df):
#     df = df.drop(df.index[0])
#     return df


def build_graph(df):
    G = nx.Graph()

 # Add nodes with attributes
    df.apply(lambda row: G.add_node(row[ROBOT_ID_COL], 
                                     X=row[X_COL], 
                                     Y=row[Y_COL], 
                                     heading=row[HEADING_COL], 
                                     is_faulty=row[IS_FAULTY_COL]), axis=1)

    # Add edges
    edges = df.assign(neighbors=df[NEIGHBORS_COL].str.split()).explode('neighbors')
    G.add_edges_from(edges[[ROBOT_ID_COL, 'neighbors']].values)

    return G

def build_graphs(df, num_rows_per_timestep):
    # df = data_cleaning(df)

    G = []
    for i in range(0, len(df), num_rows_per_timestep):
        df_subset = df[i:i+num_rows_per_timestep]
        G.append((build_graph(df_subset), df_subset))
    return G
        
        
class SharedNumpyArray:
    '''
    Wraps a numpy array so that it can be shared quickly among processes,
    avoiding unnecessary copying and (de)serializing.
    '''
    def __init__(self, array):
        '''
        Creates the shared memory and copies the array therein
        '''
        # create the shared memory location of the same size of the array
        self._shared = SharedMemory(create=True, size=array.nbytes)
        
        # save data type and shape, necessary to read the data correctly
        self._dtype, self._shape = array.dtype, array.shape
        
        # create a new numpy array that uses the shared memory we created.
        # at first, it is filled with zeros
        res = np.ndarray(
            self._shape, dtype=self._dtype, buffer=self._shared.buf
        )
        
        # copy data from the array to the shared memory. numpy will
        # take care of copying everything in the correct format
        res[:] = array[:]

    def read(self):
        '''
        Reads the array from the shared memory without unnecessary copying.
        '''
        # simply create an array of the correct shape and type,
        # using the shared memory location we created earlier
        return np.ndarray(self._shape, self._dtype, buffer=self._shared.buf)

    def copy(self):
        '''
        Returns a new copy of the array stored in shared memory.
        '''
        return np.copy(self.read_array())
        
    def unlink(self):
        '''
        Releases the allocated memory. Call when finished using the data,
        or when the data was copied somewhere else.
        '''
        self._shared.close()
        self._shared.unlink()       
    

class SharedPandasDataFrame:
    '''
    Wraps a pandas dataframe so that it can be shared quickly among processes,
    avoiding unnecessary copying and (de)serializing.
    '''
    def __init__(self, df):
        '''
        Creates the shared memory and copies the dataframe therein
        '''
        self._values = SharedNumpyArray(df.values)
        self._index = df.index
        self._columns = df.columns

    def read(self):
        '''
        Reads the dataframe from the shared memory
        without unnecessary copying.
        '''
        return pd.DataFrame(
            self._values.read(),
            index=self._index,
            columns=self._columns
        )
    
    def copy(self):
        '''
        Returns a new copy of the dataframe stored in shared memory.
        '''
        return pd.DataFrame(
            self._values.copy(),
            index=self._index,
            columns=self._columns
        )
        
    def unlink(self):
        '''
        Releases the allocated memory. Call when finished using the data,
        or when the data was copied somewhere else.
        '''
        self._values.unlink()