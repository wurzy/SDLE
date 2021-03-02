import networkx as nx
import matplotlib.pyplot as plot
import statistics as st
import numpy as np
import random

minN = 10
maxN = 500
step = 10

repeat = 30

x = []
y = []

def edgesInConnectedGraph(n):
    g = nx.Graph()
    for i in range(n):
        g.add_node(i)
    while not nx.is_connected(g):
        nodes = random.sample(range(n),2)
        g.add_edge(nodes[0],nodes[1])
    return nx.number_of_edges(g)

def meanEdges(a):
    return st.mean(a)

for i in range(minN,maxN + step,step):
    current=[]
    print(i)
    for j in range(repeat):
        edges = edgesInConnectedGraph(i)
        current.append(edges)
    mean = meanEdges(current)
    x.append(i)
    y.append(mean)

plot.plot(x,y)
plot.xlabel('Vertices')
plot.ylabel('Edges')
plot.show()