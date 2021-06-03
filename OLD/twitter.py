from chord.chord import *
from kademlia.node import *
from random import randint

M = 4

d = Chord(M)

# Add nodes
nodes = {}

#nodesK = {}

for i in range(2**M):
    nodes[i] = Node(i)
#    nodesK[i] = NodeK(4)
    d.join(nodes[i])

tables = d.updateAllFingerTables()
print(tables)

path = d.findPath(nodes[11],10)
print(path)

#d.leave(nodes[1])
#d.leave(nodes[5])
#d.leave(nodes[6])
#d.leave(nodes[11])
#tables = d.updateAllFingerTables()

#print(tables)

#path = d.findPath(nodes[11],10)
#print(path)

#for key,value in nodesK.items():
#    print(key, value._id)


#for i in range(5, 1024, 10):
#    d.store(d._startNode, i, "hello" + str(i))

#for i in range(5, 200, 10):
#    print(d.lookup(d._startNode, i))

#TIMELINE HUGO

print()
d.subscribe(nodes[11],7)
d.subscribe(nodes[11],10)
d.subscribe(nodes[11],12)

print()
d.publish(nodes[11])
d.publish(nodes[7])
d.publish(nodes[11])
d.publish(nodes[10])
d.publish(nodes[12])
d.publish(nodes[11])