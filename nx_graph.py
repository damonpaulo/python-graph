''' networkx_graph.py
implement a directed, weighted graph in a class named Graph
integrate it with networkx '''

import sys
import collections

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean

class Asset():
	def __init__(self, node_id, attributes, status, status_f):
		self.status = status
		self.status_f = status_f
		self.attributes = attributes
		self.category = 'asset'
		self.nid = node_id
		
	def __str__(self):
		return 'Asset ' + str(self.nid)
			
	def update_asset(self,*args):
		if len(args) == 1:
			comp_stat = [i.status for i in args[0]]
			self.status = self.status_f(comp_stat)
		else:
			self.status = self.status_f(args)

class Component():
	def __init__(self, node_id, attributes, status):
		self.status = status
		self.attributes = attributes
		self.category = 'component'
		self.nid = node_id
		
	def __str__(self):
		return 'Component ' + str(self.nid)
		
	def push_updates(self):
		return
		# could implement this to force associated assets to update

class Node(Asset, Component):	
	def __init__(self, node_id=0, neighbors=set(), children=collections.deque(), 
	             attributes=[], category='node', function=None):
		self.neighbors = neighbors
		self.attributes = attributes
		self.nid = node_id
		self.children = children
		self.category = category
		if category == 'asset':
			self.value = Asset(0, function)
		elif category == 'component':
			self.value = Component(1)
		else:
			self.value = category
	
def prep_data_for_graph(edge_file,vertex_file,asset_functions=None):
	E = pd.read_csv(edge_file)
	V = pd.read_csv(vertex_file).set_index('VERTEX')
	print('E:',E)
	# Make keys for Vertex List - V
	V['ATTRIBUTES'] = V.apply((lambda row: row['ATTRIBUTES'].split(';')), axis=1)
	print('V:',V)
	Nodes = list(V['CATEGORY'])
	
	for i, n in enumerate(Nodes):
		if n == 'asset':
			Nodes[i] = Asset(i,V.iloc[i,1],V.iloc[i,2],asset_functions[V.iloc[i,3]])
		else:
			Nodes[i] = Component(i,V.iloc[i,1],V.iloc[i,2])
	
	V['NODE'] = Nodes

	E['FROM'] = E.apply((lambda row: V.iloc[row[0]]['NODE']), axis=1)
	E['TO'] = E.apply((lambda row: V.iloc[row[1]]['NODE']), axis=1)
	return (V, E)

def main():
	#define functions
	def w_mean(*args):
		return
		#weighted mean would need weights passed
		
	
	functions = {'mean': mean, 'weighted mean': w_mean}
	
	(V, E) = prep_data_for_graph('edge_in.csv','vertex_in.csv',functions)
	
	G = nx.from_pandas_edgelist(E,source='FROM',target='TO',edge_attr='WEIGHT',create_using=nx.DiGraph())
	
	node_str = [str(node) for node in G.nodes()]
	node_type = [type(node) for node in G.nodes()]
	lbl = dict(zip(G.nodes(),node_str))
	
	col = ['palegreen' if n is Asset else 'deepskyblue' for n in node_type]
	#shp = ['h' if n is Asset else 'o' for n in node_type] #not sure if this is possible #shape options 'so^>v<dph8'
	nx.draw_circular(G, labels=lbl, with_labels=True,font_size=10,font_color='darkslategray',node_color=col,node_size=6000,node_shape='o',alpha=0.67)
	plt.savefig('graph.png')
	
	assets = list(V[V['NODE'].apply(lambda x: isinstance(x, Asset))]['NODE'])
	print(assets)
	
	for i, n in enumerate(nx.all_neighbors(G, assets[0])):
		print(i, n)
		
	for a in assets:
		print(a.status)
		a.update_asset(nx.all_neighbors(G,a))
		print(a.status)
	
	return

if __name__ == '__main__':
	sys.exit(main())