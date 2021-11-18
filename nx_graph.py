''' networkx_graph.py
implement a directed, weighted graph in a class named Graph
integrate it with networkx '''

import sys
import collections
#from numpy import array
#from numpy import genfromtxt
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Asset():
	def __init__(self, status, status_f):
		self.status = status
		self.status_f = status_f
		
	def update_asset(self,*args):
		self.status = self.status_f(args)
				
class Component():
	def __init__(self, status):
		self.status = status
		
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
			
	#def __str__(self):

	def print_children(self):
		print("Node", self.nid, "children:", list(c for c in self.children))
	
	def print_neighbors(self):
		print("Node", self.nid, "neighbors:", list(n.nid for n in self.neighbors))


			
# implement a directed, weighted graph from an edge list
class Graph(Node):
	def __init__(self, E, V=None):
		# Edge List - E
		E['EDGE'] = E.apply((lambda row: (row['FROM'], row['TO'])), axis=1)
		self.E = E
		print(E)
		
		# Make keys for Vertex List - V
		if V is None:
			V = []
			for i in E.keys():
				V.append(i[0])
				V.append(i[1])
			attributes = []
			
			V = set(V)
		V['ATTRIBUTES'] = V.apply((lambda row: row['ATTRIBUTES'].split(';')), axis=1)
		print(V)
		# Adjacency List - adj, List of Neighbors, Vertex List - V
		self.V, self.adj, self.neighbors = {}, {}, {}
		
		def dummy_func2(*args):
			num, denom = 0, 0
			
			for x in args[0]:
				num += x
				denom += 1
				
			return num/denom
			
		def dummy_func(*args):
			from statistics import mean
			return mean(args[0])
				
			
		for vertex, cat in enumerate(V['CATEGORY']):
			self.adj[vertex] = collections.deque()
			self.neighbors[vertex] = set()
			self.V[vertex] = Node(node_id=vertex, neighbors=self.neighbors[vertex], 
			                      attributes=[], children=self.adj[vertex], category=cat, function=(dummy_func))

		for f, t in E['EDGE']:#.iteritems(): # f = from vertex, t = to vertex
			self.adj[f].append(t)
			self.neighbors[f].add(self.V[t])
			self.neighbors[t].add(self.V[f])
		
	def print_graph(self):
		print('-'*50)
		print('V: ', self.V.keys())
		print('E: ', self.E)
		print('Adj: ', self.adj)
		print('Neighbors: ', list(i for i in self.neighbors))
		print('-'*50)

def main():
	G = Graph(pd.read_csv('g3.csv'),V=pd.read_csv('g3v.csv'))
	G.print_graph()
	E = G.E
	
	Gnx = nx.from_pandas_edgelist(E,source='FROM',target='TO',edge_attr='WEIGHT',create_using=nx.DiGraph())
	
	nx.draw(Gnx, with_labels=True)
	plt.savefig('graph2.png')
		
	V = G.V
	print(V[0].value.status)
	V[0].value.update_asset(V[1].value.status,V[2].value.status)
	print(V[0].value.status)

	return

if __name__ == '__main__':
	sys.exit(main())