import graphs
import random 
import networkx as nx

## 1. fazer para os nodos o numero total de saltos e extrair o maximo. Isto dá uma amostra estocastica das excentricidades. (erdos renyi e preferential attachment)
## 2. Em vez de flooding, limitar as transmissoes para um subset de vizinhos. Primeiro enviar para 100%, verificar que se chega a todos os nodos, e indo reduzindo. 

def flooding(graph, n): 
    seen = [False] * n
    nodes = range(nr_nodes)
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

nr_nodes = 100
graph1 = graphs.barabesi_albert(nr_nodes)
graph2 = graphs.erdos_renyi(nr_nodes)

counter1 = flooding(graph1, nr_nodes)
counter2 = flooding(graph2, nr_nodes)
print(counter1, nx.diameter(graph1), counter2, nx.diameter(graph2))

