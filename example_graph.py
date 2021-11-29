import nx_graph # nx_graph.py must be in same directory
from statistics import mean

edge_file, vertex_file = 'edge_in.csv', 'vertex_in.csv'
funcs = {0: None, 'mean': mean}
e_attr = ['WEIGHT','DIST']
verbose = True

(G, V, E) = nx_graph.create_graph(edge_file,vertex_file,funcs,edge_attr=e_attr,verbose=verbose)