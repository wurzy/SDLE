import graphs
import random 
import networkx as nx
import matplotlib.pyplot as plot

## 1. fazer para os nodos o numero total de saltos e extrair o maximo. Isto dá uma amostra estocastica das excentricidades. (erdos renyi e preferential attachment)
## 2. Em vez de flooding, limitar as transmissoes para um subset de vizinhos. Primeiro enviar para 100%, verificar que se chega a todos os nodos, e indo reduzindo. 

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

def gossip(graph, n): 
    pass

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

flooding_plot(nr_nodes)