import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from collections import Counter

def calculate(degree_array):
    total = sum(degree_array)
    size = len(degree_array)
    result = [None] * size
    for i in range(0, size):
        result[i] = degree_array[i]/total
    return np.random.choice(np.arange(0, size), p=result)

graph = nx.Graph()
nodes = int(input("Insert number of nodes: "))
graph.add_nodes_from(range(0, nodes))
isConnected = False
# initialize arrays of the node degree and normalized probability
initial = np.full(nodes, 1)
degrees = np.full(nodes, 1)
# array = list(range(0, nodes))
# start algorithm
while not isConnected:
    # assume origin node u has weights of 1 on each node
    u = calculate(initial)
    v = calculate(degrees)
    # array, v = random(array)
    if not graph.has_edge(u, v) and not u == v:
        graph.add_edge(u, v)
        degrees[v] += 1
        isConnected = nx.is_connected(graph)
    print(degrees)

sorted_by_degree = sorted(graph.degree(), key=lambda var: var[1], reverse=True)
x, height = zip(*sorted_by_degree)

print("XX")
print(x,height)
print(sorted_by_degree)
stats = Counter(degrees).most_common()
print(stats)