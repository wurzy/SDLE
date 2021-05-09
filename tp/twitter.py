from dht.dht import *
from random import randint

d = DHT(5)

# Add nodes
for i in range(32):
    d.join(Node(i))

tables = d.updateAllFingerTables()
print(tables)


#for i in range(5, 1024, 10):
#    d.store(d._startNode, i, "hello" + str(i))

#for i in range(5, 200, 10):
#    print(d.lookup(d._startNode, i))