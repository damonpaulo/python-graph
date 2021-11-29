'''
example_graph.py

import nx_graph.py
create a networkx graph G based on user defined input
'''

import nx_graph # nx_graph.py must be in same directory
from statistics import mean

# user defined input
edge_file, vertex_file = 'edge_in.csv', 'vertex_in.csv'
funcs = {0: None, 'mean': mean}
e_attr = ['WEIGHT','DIST']
verbose = False

# creates 3 variables:
#   G is a NetworkX DiGraph
#   V is a pandas dataframe containing the detailed vertex data
#   E is a pandas dataframe containing the detailed edge data
sim = nx_graph.Simulator(edge_file,vertex_file,funcs,e_attr,verbose=verbose)

print(sim.V)
print(sim.E)