from dht.dht import *
from random import randint

d = DHT(4)

# Add nodes
nodes = {}
for i in range(16):
    nodes[i] = Node(i)
    d.join(nodes[i])

tables = d.updateAllFingerTables()
print(tables)

path = d.findPath(nodes[11],10)
print(path)

#for i in range(5, 1024, 10):
#    d.store(d._startNode, i, "hello" + str(i))

#for i in range(5, 200, 10):
#    print(d.lookup(d._startNode, i))