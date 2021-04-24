import graphs
import random 
import networkx as nx
import matplotlib.pyplot as plot
import numpy as np

nr_nodes = 100

def flooding(graph, n): 
    seen = [False] * n
    nodes = range(n)
    root = random.choice(nodes)
    neighbors = list(graph.neighbors(root))
    seen[root] = True
    counter = 0

    while False in seen:
        new_neighbors = []
        for node in neighbors: 
            if not seen[node]:
                new_neighbors += list(graph.neighbors(node))
                seen[node] = True
        counter += 1
        neighbors = new_neighbors

    return counter

def gossip_select(neighbors, probability):
    mask = np.random.binomial(1, probability, len(neighbors))
    result = [elem for keep, elem in zip(mask, neighbors) if keep]
    if not result:
        result.append(neighbors[0])
    return result

def gossip(graph, n, percentage): 
    seen = [False] * n
    nodes = range(n)
    root = random.choice(nodes)
    neighbors = list(graph.neighbors(root))
    new_neighbors = neighbors
    seen[root] = True
    counter = 0

    while len(neighbors) > 0 and False in seen:
        new_neighbors = []
        for node in neighbors: 
            if not seen[node]:
                new_neighbors += gossip_select(list(graph.neighbors(node)),percentage)
                seen[node] = True
        counter += 1
        neighbors = new_neighbors
    return sum(i == True for i in seen) / n

def flooding_plot(nr_nodes): 
    iterations = range(nr_nodes + 1)
    x, y1, y2 = [], [], []
    graph1, graph2 = None, None

    for i in iterations[2:]:
        x.append(i)
        graph1 = graphs.erdos_renyi(i)
        y1.append(flooding(graph1, i))
        graph2 = graphs.barabesi_albert(i)
        y2.append(flooding(graph2, i))

    plot.subplot(2, 2, 1)
    plot.scatter(x, y1)
    plot.xlabel('Nodes')
    plot.ylabel('# iterations (Erdos-Renyi)')

    plot.subplot(2, 2, 2)
    plot.scatter(x, y2)
    plot.xlabel('Nodes')
    plot.ylabel('# iterations (Barabesi-Albert)')

    plot.subplot(2, 2, 3)
    nx.draw(graph1,node_size=60,font_size=8) 

    plot.subplot(2, 2, 4)
    nx.draw(graph2,node_size=60,font_size=8) 
    plot.show()

def gossip_plot(nr_nodes): 
    percentages = np.arange(0.1, 1.1, 0.1)
    x, y1, y2 = [], [], []
    graph1 = graphs.erdos_renyi(nr_nodes)
    graph2 = graphs.barabesi_albert(nr_nodes)

    for percentage in percentages:
        x.append(percentage)
        y1.append(gossip(graph1, nr_nodes, percentage))
        y2.append(gossip(graph2, nr_nodes, percentage))

    plot.subplot(2, 2, 1)
    plot.scatter(x, y1)
    plot.xlabel('% Subset')
    plot.ylabel('% nodes (Erdos-Renyi)')

    plot.subplot(2, 2, 2)
    plot.scatter(x, y2)
    plot.xlabel('% Subset')
    plot.ylabel('% nodes (Barabesi-Albert)')

    plot.subplot(2, 2, 3)
    nx.draw(graph1,node_size=60,font_size=8) 

    plot.subplot(2, 2, 4)
    nx.draw(graph2,node_size=60,font_size=8) 
    plot.show()

gossip_plot(100)