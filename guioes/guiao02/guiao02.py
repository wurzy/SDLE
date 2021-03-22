import networkx as nx
import matplotlib.pyplot as plot
import statistics as st
from collections import Counter
import random

minN = 10
maxN = 100
step = 1

repeat = 30

nodes = []
edges = []

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
def preferentialAttachment(n):
    nodes = []
    edges = []
    g = nx.Graph()
    choices = [0]
    for u in range(1,n):
        g.add_node(u)
        v = random.choice(choices)
        choices.append(u)
        choices.append(u)
        choices.append(v)
        g.add_edge(u,v)
    return g

cur = []
g = None
for n in range(minN, maxN + step, step):
    for i in range(repeat):
        g = preferentialAttachment(n)
        cur.append(nx.number_of_edges(g))
    nodes.append(n)
    edges.append(st.mean(cur))


plot.subplot(2, 2, 1)
plot.plot(nodes,edges)
plot.xlabel('Nodes')
plot.ylabel('# edges')
plot.axis('scaled')

x,y = nodesByDegree(g)

plot.subplot(2, 2, 2)
plot.bar(x, y, align='center')
plot.xlabel('Degree')
plot.ylabel('# of nodes')
plot.title('Degree Distribution')

plot.subplot(2, 2, 3)
plot.scatter(x,y)
plot.xlabel('(log) Degree')
plot.ylabel('(log) # of nodes')
plot.yscale('log')
plot.xscale('log')

plot.subplot(2,2,4)
nx.draw(g,node_size=60,font_size=8) 

plot.show()