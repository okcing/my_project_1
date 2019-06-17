#coding=utf8
import networkx as nx
import time
import cPickle as pickle
import ujson
from collections import defaultdict


start = time.time()
G = nx.read_edgelist('../data/construct_train_data/user_item_edgelist_10h_filter', nodetype=str)
print time.time() - start

nodes = G.nodes()
print(type(nodes))
nodes = list(G.nodes())
print len(nodes)

node_neighbors = defaultdict(list)

for index, node in enumerate(nodes):
    nodes = G.neighbors(node)
    for n in nodes:
        node_neighbors[node].append(n)


# 存储图的邻居
start = time.time()
with open('../data/construct_train_data/user_item_edgelist_10h_filter.json', 'w') as json_file:
    ujson.dump(node_neighbors, json_file)
print time.time() - start
