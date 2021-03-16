import networkx as nx
import matplotlib.pyplot as plot
from collections import Counter
import random

minN = 1
maxN = 30

nodes = []
edges = []

def unfoldDegrees(graph):
    degrees = []
    for (node,val) in graph.degree(): # [ (1,2), (3,2) ] => [1, 1, 3, 3]
        repeat = [val] * (node + 1) 
        degrees = degrees + repeat 
    return degrees

def nodesByDegree(graph):
    x = []
    y = []
    degrees = [val for (node, val) in graph.degree()]
    count = Counter(degrees).most_common() #[(1, 24), (2, 2), (4, 4)]
    for (d,n) in count:
        x.append(d)
        y.append(n)
    return x,y

# returns preferred node for attachment
def preferentialAttachment(graph,u):
    degrees = unfoldDegrees(graph)
    v = random.choice(degrees)
    while graph.has_edge(u,v) or u==v: # dont allow repeated edges; must be different nodes
        v = random.choice(degrees)
    return v

g = nx.Graph()
for u in range(minN,maxN+1):
    g.add_node(u)
    while not nx.is_connected(g):
        v = preferentialAttachment(g,u)
        g.add_edge(u,v)
    nodes.append(u)
    edges.append(nx.number_of_edges(g))

nx.draw(g,with_labels=True)
plot.draw()
plot.show()

plot.plot(nodes,edges)
plot.xlabel('Nodes')
plot.ylabel('# edges')
plot.axis('scaled')
plot.show()

x,y = nodesByDegree(g)

plot.bar(x, y, align='center')
plot.xlabel('Degree')
plot.ylabel('# of nodes')
plot.title('Degree Distribution')
plot.show()

plot.scatter(x,y)
plot.yscale('log')
plot.xscale('log')
plot.show()