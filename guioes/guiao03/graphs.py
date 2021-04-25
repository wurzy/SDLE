import networkx as nx
import random
from itertools import combinations
from random import choice, sample

def erdos_renyi(n):
    g = nx.Graph()
    for i in range(n):
        g.add_node(i)
    while not nx.is_connected(g):
        nodes = random.sample(range(n),2)
        g.add_edge(nodes[0],nodes[1])
    return g

def barabesi_albert(n):
    nodes = []
    edges = []
    g = nx.Graph()
    choices = [0]
    for u in range(1,n):
        g.add_node(u)
        v = random.choice(choices)
        choices.append(u)
        choices.append(v)
        g.add_edge(u,v)
    return g

def barabesi_albert_redundance(n):
    nodes = []
    edges = []
    g = nx.Graph()
    choices = [0]
    for u in range(1,n):
        g.add_node(u)
        v = random.choice(choices)
        choices.append(u)
        choices.append(v)
        g.add_edge(u,v)
    # needs redundance otherwise using a percentage of the subset will result in poor results
    for u in range(1,n):
        g.add_node(u)
        v = random.choice(choices)
        choices.append(u)
        choices.append(v)
        g.add_edge(u,v)
    return g