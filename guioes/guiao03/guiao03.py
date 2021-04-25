import graphs
import random 
import networkx as nx
import matplotlib.pyplot as plot
import numpy as np

nr_nodes = 100
repeat = 30

def remove_duplicates(l):
    return list(set(l))

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

def gossip_select(neighbors, percentage):
    mask = np.random.binomial(1, percentage, len(neighbors))
    result = [elem for keep, elem in zip(mask, neighbors) if keep]
    if not result:
        result.append(neighbors[0])
    return result
    #k = int(round(len(neighbors)*percentage))
    #indexes = random.sample(range(len(neighbors)),k)
    #return [neighbors[i] for i in indexes]

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
        neighbors = remove_duplicates(new_neighbors)

    return sum(i == True for i in seen) / n

def flooding_plot(nr_nodes): 
    iterations = range(nr_nodes + 1)
    x, y1, y2 = [], [], []
    graph1, graph2 = None, None

    for i in iterations[2:]:
        x.append(i)
        avg1, avg2 = [], []
        for j in range(repeat):
            graph1 = graphs.erdos_renyi(i)
            avg1.append(flooding(graph1, i))
            graph2 = graphs.barabesi_albert(i)
            avg2.append(flooding(graph2, i))
        y1.append( sum(avg1) / repeat )
        y2.append( sum(avg2) / repeat )

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
    graph2 = graphs.barabesi_albert_redundance(nr_nodes)

    for percentage in percentages:
        avg1, avg2 = [], []
        x.append(percentage)
        for j in range(repeat): 
            avg1.append(gossip(graph1, nr_nodes, percentage))
            avg2.append(gossip(graph2, nr_nodes, percentage))
        y1.append( sum(avg1) / repeat )
        y2.append( sum(avg2) / repeat )

    plot.subplot(2, 2, 1)
    plot.scatter(x, y1)
    plot.xlabel('% Subset')
    plot.ylabel('% ' + str(nr_nodes) + ' nodes (Erdos-Renyi)')

    plot.subplot(2, 2, 2)
    plot.scatter(x, y2)
    plot.xlabel('% Subset')
    plot.ylabel('% ' + str(nr_nodes) + ' nodes (Barabesi-Albert)')

    plot.subplot(2, 2, 3)
    nx.draw(graph1,node_size=60,font_size=8) 

    plot.subplot(2, 2, 4)
    nx.draw(graph2,node_size=60,font_size=8) 
    plot.show()

gossip_plot(nr_nodes)
#flooding_plot(nr_nodes)