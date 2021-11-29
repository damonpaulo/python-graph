''' 
networkx_graph.py

implements a directed, weighted graph of custom nodes
  implements a custom node class to represent system components
  implements a function to create a networkx graph of custom nodes
  based on data defined in 2 .csv files
	'edge_in.csv' is an edge list
	'vertex_in.csv' is a vertex list
  user may provide functions to be associated with nodes
'''

import sys
import collections

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# implement a custom node class
# nodes may be assigned:
	# a category (str)
	# attributes (list)
	# status (int)
	# node_id(nid) - (int)
	# function (func)
class Node():	
	def __init__(self, node_id=0, category='node', attributes=[], status=0, function=None):
		self.nid = node_id
		self.category = category
		self.attributes = attributes
		self.category = category
		self.status = status
		self.function = function
		
	def __repr__(self):
		return 'Node obj.: '+repr(self.nid)
		
	def __str__(self):
		return self.category.capitalize()+' '+str(self.nid)
		
	# pass in-neighbors as args
	# expects to be passed a single argument -- G.predecesors(n)
	# will simply pass exact provided args to the function if other than 1 argument
	def update_node(self,*args):
		if len(args) == 1:
			comp_stat = [i.status for i in args[0]]
			self.status = self.function(comp_stat)
		else:
			self.status = self.function(args)

	# pass in-edges as args
	# expects to be passed a single argument -- G.in_edges(n,data=True)
	# expects data to include a 'WEIGHT' column, ignores any other data if it exists (i.e., 'DIST')
	# will simply pass exact provided args to the function if other than 1 argument
	def update_node_weighted(self,*args):
		if len(args) == 1:
			stat_weight = [(i[0].status, i[2]['WEIGHT']) for i in args[0]]
			self.status = self.function(stat_weight)
		else:
			self.status = self.function(args)

class Simulator(Node):
	def __init__(self,edge_file,vertex_file,asset_functions,e_attr=[],verbose=False):
		(self.G, self.V, self.E) = self.create_graph(edge_file,vertex_file,asset_functions,e_attr,verbose)
			
	def create_graph(self,edge_file,vertex_file,asset_functions,edge_attr,verbose=False):
		E = pd.read_csv(edge_file)
		V = pd.read_csv(vertex_file).set_index('VERTEX')
		if verbose: print('E:\n',E,'\n')
		# to allow lists within attributes use ';' since ',' is delimiter in file read
		V['ATTRIBUTES'] = V.apply((lambda row: row['ATTRIBUTES'].split(';')), axis=1)
		# user can leave function value blank and we will fill with 0's to link to null function
		V['FUNCTION'] = V['FUNCTION'].fillna(0)
		Nodes = []
	
		for i in range(len(V)):
			Nodes.append(Node(i,V.iloc[i,0],V.iloc[i,1],V.iloc[i,2],asset_functions[V.iloc[i,3]]))
	
		V['NODE'] = Nodes
		if verbose: print('V:\n',V,'\n')

		E['FROM'] = E.apply((lambda row: V.iloc[row[0]]['NODE']), axis=1)
		E['TO'] = E.apply((lambda row: V.iloc[row[1]]['NODE']), axis=1)
	
		# create a NetworkX graph from provided inputes
		# uses a Directed Graph (nx.DiGraph) -- no options at this time for any other kind of graph
		G = nx.from_pandas_edgelist(E,source='FROM',target='TO',edge_attr=edge_attr,create_using=nx.DiGraph())

		return (G, V, E)
		
	# Iterate over all nodes and run update functions
	def update_nodes(self):
		return

# example defined in main
def main():
	# if not verbose there is no output
	# if verbose then E and V will be output
	verbose = True
	
	# define example you want
	# currently support 'ex1' or 'ex2'
	example = 'ex2'
	
	if example == 'ex2':
		edge_file, vertex_file = 'edge_in_2.csv', 'vertex_in_2.csv'
	else:
		edge_file, vertex_file = 'edge_in.csv', 'vertex_in.csv'
	
	# import mean function
	from statistics import mean
	
	# define a weighted mean function
	def w_mean(*args):
		stat_weight = args[0]
		num, denom = 0, 0
		for (s, w) in stat_weight:
			num += s*w
			denom += w
			
		return num/denom
	
	# users provide a dictionary that associates a string value to a python function
	# expected use, vertex_in.csv includes a 'FUNCTION' column where the desired function
	#   is listed as a string -- the user then defines the function in their code and passes
	#   the dictionary containing these functions to the create_graph() function
	# (need 0: None for null function in current version)
	functions = {0: None, 'mean': mean, 'wmean': w_mean}
	
	# user must define the attributes to be stored on each edge
	# in this case we have a weight and distance
	# these columns will be included with any values in the edge input .csv file
	edge_attr = ['WEIGHT','DIST']
	sim = Simulator(edge_file,vertex_file,functions,e_attr=edge_attr,verbose=verbose)
		
	(G, V, E) = (sim.G, sim.V, sim.E)
	# sample way to separate different categories of nodes
	# in this case nodes are an 'asset' or a 'component'
	assets = V['NODE'].loc[V['CATEGORY']=='asset']
	components = V['NODE'].loc[V['CATEGORY']=='component']
	
	# sample way to iterate over all assets and updates
	# this should be an option for a user defined simulator object
	for a in assets:
		if verbose: print('Status of',a,'before update:',a.status)
		if example == 'ex2':
			a.update_node_weighted(G.in_edges(a,data=True))
		else:
			a.update_node(G.predecessors(a))
		
		if verbose: print('Status of',a,'after  update:',a.status,'\n')
	
	# sample way to draw graph 
	# if we want to support graphing there are more full featured libraries than the built-in
	#   NetworkX draw() functions which are built on matplotlib.pyplot
	# could implement support to draw in our graph function if it would be a useful feature
	col = ['deepskyblue' if n.category=='asset' else 'gray' for n in G.nodes()]
	nx.draw_spectral(G, with_labels=True,font_size=10,node_color=col,node_size=5000,node_shape='o',alpha=0.7)
	plt.savefig('graph-'+example+'.png')
	
	return
	
if __name__ == '__main__':
	sys.exit(main())