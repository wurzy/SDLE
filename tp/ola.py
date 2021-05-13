k = 4

class Node:
    def __init__(self, id, k):
        self.id = id
        self.size = 2**k
        self.data = {}
        #self.finger = [ ( self.id + 2**(x-1) ) % self.size for x in range(1,k+1) ]
        #self.finger = [ self.id ^ 2**x for x in range(k) ]
        self.finger = {}

    def createFingerTable(self,nodes:dict,k,type):
        if type=='Chord':
            self.finger = { ( self.id + 2**(x-1) ) % self.size: nodes[( self.id + 2**(x-1) ) % self.size] for x in range(1,k+1) }
        if type=='Kademlia':
            self.finger = [ nodes[self.id ^ 2**x] for x in range(k) ]

    def printTables(self):
        succ = [ x for x in self.finger.keys()]
        tables = [ x.id for x in self.finger.values()]
        print("ID " + str(self.id) + ": ", succ, " -> ", tables)


# This is a clockwise ring distance function.
# It depends on a globally defined k, the key size.
# The largest possible node id is 2**k.
def distance(a, b):
    if a==b:
        return 0
    elif a<b:
        return b-a
    else:
        return (2**k)+(b-a)

def findFinger(node, key):
    current=node

    for x in node.finger.values():
        if distance(current.id, key.id) > distance(x.id, key.id):
            current = x

    return current

def lookup(start, goal):
    table = []
    table.append(start.id)
    current=findFinger(start, goal)
    table.append(current.id)
    next=findFinger(current, goal)
    while distance(current.id, goal.id) > distance(next.id, goal.id):
        current=next
        next=findFinger(current, goal)
        table.append(current.id)
    return table


#def findNode(start, goal, nodes):
#    current=start
#    found = False
#    if goal in current.finger:
#        return goal
#    while not found:
#        for finger in current.finger:
#
#    #while distance(current.id, key) > distance(current.next.id, key):
#    #    current=current.next
#    return current    

def leave(node, nodes: dict):
    for n in nodes.values():
        for succ,finger in n.finger.items():
            if finger.id == node.id:
                n.finger[succ] = nodes[next(iter(nodes[finger.id].finger))]
    del nodes[node.id]

def main():
    nodes = {}
    for i in range(2**k):
        nodes[i] = Node(i,k) 
    for i in range(2**k):
        nodes[i].createFingerTable(nodes,4,"Chord")
    
    #lookup(nodes[11],nodes[10])
    lookup(nodes[11],nodes[7])
    table = lookup(nodes[11],nodes[7])
    print(table)
    print("Hops:", len(table)-1)
    #leave(nodes[1],nodes)
    #leave(nodes[2],nodes)
    #leave(nodes[4],nodes)
    #leave(nodes[8],nodes)
    leave(nodes[3],nodes)
    table = lookup(nodes[11],nodes[7])
    print(table)
    print("Hops:", len(table)-1)
    #for i in nodes.values():
       # i.printTables()

if __name__ == '__main__':
    main()