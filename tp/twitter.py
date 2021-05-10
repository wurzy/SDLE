from chord.chord import *
from kademlia.node import *
from random import randint

d = Chord(4)

# Add nodes
nodes = {}

#nodesK = {}

for i in range(16):
    nodes[i] = Node(i)
#    nodesK[i] = NodeK(4)
    d.join(nodes[i])

tables = d.updateAllFingerTables()
print(tables)

path = d.findPath(nodes[11],10)
print(path)

#for key,value in nodesK.items():
#    print(key, value._id)


#for i in range(5, 1024, 10):
#    d.store(d._startNode, i, "hello" + str(i))

#for i in range(5, 200, 10):
#    print(d.lookup(d._startNode, i))