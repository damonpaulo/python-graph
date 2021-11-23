''' networkx_graph.py
implement a directed, weighted graph in a class named Graph
integrate it with networkx '''

import sys
import collections

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean

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
	def update_node(self,*args):
		if len(args) == 1:
			comp_stat = [i.status for i in args[0]]
			self.status = self.function(comp_stat)
		else:
			self.status = self.function(args)

	#pass in-edges as args
	def update_node_weighted(self,*args):
		if len(args) == 1:
			stat_weight = [(i[0].status, i[2]['WEIGHT']) for i in args[0]]
			self.status = self.function(stat_weight)
		else:
			self.status = self.function(args)
			
	
def prep_data_for_graph(edge_file,vertex_file,asset_functions):
	E = pd.read_csv(edge_file)
	V = pd.read_csv(vertex_file).set_index('VERTEX')
	print('E:\n',E,'\n')
	V['ATTRIBUTES'] = V.apply((lambda row: row['ATTRIBUTES'].split(';')), axis=1)
	V['FUNCTION'] = V['FUNCTION'].fillna(0)
	Nodes = []
	
	
	for i in range(len(V)):
		Nodes.append(Node(i,V.iloc[i,0],V.iloc[i,1],V.iloc[i,2],asset_functions[V.iloc[i,3]]))
	
	V['NODE'] = Nodes
	print('V:\n',V,'\n')

	E['FROM'] = E.apply((lambda row: V.iloc[row[0]]['NODE']), axis=1)
	E['TO'] = E.apply((lambda row: V.iloc[row[1]]['NODE']), axis=1)
	return (V, E)

def main():
	#define example you want
	example = 'ex2'
	
	def w_mean(*args):
		stat_weight = args[0]
		num, denom = 0, 0
		for (s, w) in stat_weight:
			num += s*w
			denom += w
			
		return num/denom
		
	#define functions in python based on string input (need 0: None for null function)
	functions = {0: None, 'mean': mean, 'wmean': w_mean}
	
	if example == 'ex2':
		edge_file, vertex_file = 'edge_in_2.csv', 'vertex_in_2.csv'
	else:
		edge_file, vertex_file = 'edge_in.csv', 'vertex_in.csv'
	
	(V, E) = prep_data_for_graph(edge_file,vertex_file,functions)
	
	G = nx.from_pandas_edgelist(E,source='FROM',target='TO',edge_attr=['WEIGHT','DIST'],create_using=nx.DiGraph())
	#print(G.edges.data())
	
	assets = V['NODE'].loc[V['CATEGORY']=='asset']
	components = V['NODE'].loc[V['CATEGORY']=='component']
		
	for a in assets:
		print('Status of',a,'before update:',a.status)
		if example == 'ex2':
			a.update_node_weighted(G.in_edges(a,data=True))
			for e in G.in_edges(a,data=True):
				print(e)
		else:
			a.update_node(G.predecessors(a))
		
		print('Status of',a,'after  update:',a.status,'\n')
	
	#draw graph
	col = ['palegreen' if n.category=='asset' else 'deepskyblue' for n in G.nodes()]
	nx.draw_spectral(G, with_labels=True,font_size=10,node_color=col,node_size=5000,node_shape='o',alpha=0.7)
	plt.savefig('graph-'+example+'.png')
	
	
	return
	
if __name__ == '__main__':
	sys.exit(main())