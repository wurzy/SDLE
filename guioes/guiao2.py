import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import random


# draw erdos-renyi connected graph
def erdos_renyi(num_vertices):
    G = nx.Graph()
    for i in range(num_vertices):
        G.add_node(i)
    while not nx.is_connected(G):
        a = randrange(num_vertices)
        b = randrange(num_vertices)
        while b == a:
            b = randrange(num_vertices)
        G.add_edge(a,b)
    return nx.number_of_edges(G)
    # nx.draw(G)
    # plt.show()



# decides if an edge is created or not based on probability
def decision(probability):
    return random.random() < probability

# return list composed by each node's probability of edge creation
def calc_probabilities(graph):
    probs = []
    degrees = []
    for x in list(graph):
        degrees.append(graph.degree(x))

    sum_degree = sum(degrees)

    for x in list(graph):
        if sum_degree == 0:
            probability = 1
        else:
            probability = degrees[x] / sum_degree
        probs.append(probability)

    return probs

# draw erdos-renyi connected graph
def barabasi_albert(num_vertices):
    G = nx.Graph()
    probability = []
    for i in range(num_vertices):
        G.add_node(i)
        probability = calc_probabilities(G)
        while not nx.is_connected(G):
            for node in list(G):
                if decision(probability[node]):
                    G.add_edge(i,node)
                    probability = calc_probabilities(G)
                    break
    return nx.number_of_edges(G)
    # nx.draw(G,node_size=10)
    # plt.show()

def barabasi_albert_v2(num_vertices):
    G = nx.Graph()
    probability = []
    for i in range(num_vertices):
        G.add_node(i)

    probability = calc_probabilities(G)
    while not nx.is_connected(G):
        a = randrange(num_vertices)
        b = randrange(num_vertices)
        while b == a:
            b = randrange(num_vertices)
        if decision(probability[b]):
            G.add_edge(a,b)
            probability = calc_probabilities(G)
    return nx.number_of_edges(G)
    # nx.draw(G)
    # plt.show()


def draw_graph(num_times):
    x_vertices = [8,32,64,128,256,512]
    
    y_mean = []
    for i in x_vertices:
        results = []
        for x in range(num_times):
            results.append(barabasi_albert(i))
        y_mean.append(np.mean(results))
    plt.plot(x_vertices,y_mean,label='barabasi-albert')

    y_mean = []
    for i in x_vertices:
        results = []
        for x in range(num_times):
            results.append(barabasi_albert_v2(i))
        y_mean.append(np.mean(results))
    plt.plot(x_vertices,y_mean,label='barabasi-albert_v2')

    y_mean = []
    for i in x_vertices:
        results = []
        for x in range(num_times):
            results.append(erdos_renyi(i))
        y_mean.append(np.mean(results))
    plt.plot(x_vertices,y_mean,label='erdos-renyi')


    plt.xlabel('Vertices')
    plt.xticks(x_vertices)
    plt.ylabel('Edges')
    plt.legend(loc='best')
    plt.show()


# erdos_renyi(20)
# draw_graph(100)
# print(barabasi_albert_v2(100))
draw_graph(10)