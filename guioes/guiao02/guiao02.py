import networkx as nx
import matplotlib.pyplot as plot
import numpy as np
from collections import Counter
import random

minN = 10
maxN = 100
step = 10
repeat = 1

def getRandomNodes1(graph): # { (1,3) , (2,5) } => 1,1,1,2,2,2,2,2 => random = (1,2)
    degrees = []
    for (node,val) in graph.degree():
        repeat = [node] * (val + 1)
        degrees = degrees + repeat 
    print(graph.degree())
    nodes = random.sample(degrees,2)
    while graph.has_edge(nodes[0],nodes[1]):
        nodes = random.sample(degrees,2) # dont allow repeated edges; must be different nodes
    return nodes

def getRandomNodes(degrees):
    total = sum(degrees)
    size = len(degrees)
    result = []
    for i in range(size):
        result.append(degrees[i]/total) # creating probability array
    return np.random.choice(range(0,size), p=result) # uniformly choosing nodes

    
def edgesInPreferentialGraph(n):
    g = nx.Graph()
    g.add_nodes_from(range(0,n))
    degrees = [1] * n
    while not nx.is_connected(g):
        u = random.choice(list(g.nodes()))
        v = getRandomNodes(degrees)
        if not g.has_edge(u, v) and not u == v:
            g.add_edge(u, v)
            degrees[v] += 1
    stats = Counter(degrees).most_common()
    print(stats)

for i in range(minN,maxN + step,step):
    for j in range(repeat):
        edges = edgesInPreferentialGraph(i)
