''' networkx_graph.py
implement a directed, weighted graph in a class named Graph
integrate it with networkx '''

import sys
import collections

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Asset():
	def __init__(self, attributes, status, status_f):
		self.status = status
		self.status_f = status_f
		self.attributes = attributes
		self.category = 'asset'
			
	def update_asset(self,*args):
		self.status = self.status_f(args)

class Component():
	def __init__(self, attributes, status):
		self.status = status
		self.attributes = attributes
		self.category = 'component'
		
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
	print(E)
	# Make keys for Vertex List - V
	V['ATTRIBUTES'] = V.apply((lambda row: row['ATTRIBUTES'].split(';')), axis=1)
	print(V)
	Nodes = list(V['CATEGORY'])
	
	for i, n in enumerate(Nodes):
		#print(V.iloc[i,2:])
		#print(n)
		if n == 'asset':
			Nodes[i] = Asset(V.iloc[i,1],V.iloc[i,2],V.iloc[i,3])
		else:
			Nodes[i] = Component(V.iloc[i,1],V.iloc[i,2])
	
	V['NODE'] = Nodes
	
	for idx, row in E.iterrows():
		print(idx, row)
		
	E['FROM'] = E.apply((lambda row: V.iloc[row[0]]['NODE']), axis=1)
	E['TO'] = E.apply((lambda row: V.iloc[row[1]]['NODE']), axis=1)
	return E

def main():
	#G = Graph(pd.read_csv('g3.csv'),V=pd.read_csv('g3v.csv'))
	#G.print_graph()
	#E = G.E
	
	#Gnx = nx.from_pandas_edgelist(E,source='FROM',target='TO',edge_attr='WEIGHT',create_using=nx.DiGraph())
	
	#nx.draw(Gnx, with_labels=True)
	#plt.savefig('graph2.png')
		
	#V = G.V
	#print(V[0].value.status)
	#V[0].value.update_asset(V[1].value.status,V[2].value.status)
	#print(V[0].value.status)
	G = nx.from_pandas_edgelist(prep_data_for_graph('edge_in.csv','vertex_in.csv'),source='FROM',target='TO',edge_attr='WEIGHT',create_using=nx.DiGraph())
	
	nx.draw(G, with_labels=True)
	plt.savefig('graph3.png')
	
	return

if __name__ == '__main__':
	sys.exit(main())