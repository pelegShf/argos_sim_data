###############################################################################
# Run Betweenness Centrality on a large citation graph using NetworkX
import sys
import time
 
import networkx as nx
import pandas as pd
 
k = int(sys.argv[1])
 
# Dataset from https://snap.stanford.edu/data/cit-Patents.txt.gz
print("Reading dataset into Pandas DataFrame as an edgelist...", flush=True,
      end="")
pandas_edgelist = pd.read_csv(
    "./single_experiment_analysis/cit-Patents.txt",
    skiprows=4,
    delimiter="\t",
    names=["src", "dst"],
    dtype={"src": "int32", "dst": "int32"},
)
print("done.", flush=True)
print("Creating Graph from Pandas DataFrame edgelist...", flush=True, end="")
G = nx.from_pandas_edgelist(
    pandas_edgelist, source="src", target="dst", create_using=nx.DiGraph
)
print("done.", flush=True)
 
print("Running betweenness_centrality...", flush=True, end="")
st = time.time()
bc_result = nx.betweenness_centrality(G, k=k)
print(f"done, BC time with {k=} was: {(time.time() - st):.6f} s")