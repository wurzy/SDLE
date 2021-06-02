class ChordNode:
    def __init__(self, id, k, type):
        self.id = id
        self.type = type
        self.k = k
        self.size = 2**k
        self.data = {}
        if type == 'Chord':
            self.finger = { ( self.id + 2**(x-1) ) % self.size: None for x in range(1,k+1) }
        #if type == 'Kademlia':
            #self.finger = 

    def createFingerTable(self,nodes:dict):
        if self.type=='Chord':
            self.finger = { ( self.id + 2**(x-1) ) % self.size: nodes[( self.id + 2**(x-1) ) % self.size] for x in range(1,self.k+1) }
        if self.type=='Kademlia':
            self.finger = [ nodes[self.id ^ 2**x] for x in range(self.k) ]

    def printTables(self):
        succ = [ x for x in self.finger.keys()]
        tables = [ x.id for x in self.finger.values()]
        print("ID " + str(self.id) + ": ", succ, " -> ", tables)

class Chord: 
    def __init__(self,k):
        self.k = k
        self.size = 2**k
        self.nodes = {}
        for i in range(2**k):
            self.nodes[i] = ChordNode(i,k,"Chord") 
        for i in range(2**k):
            self.nodes[i].createFingerTable(self.nodes)

# This is a clockwise ring distance function.
# It depends on a globally defined k, the key size.
# The largest possible node id is 2**k.
    def distance(self, a, b):
        if a==b:
            return 0
        elif a<b:
            return b-a
        else:
            return (2**self.k)+(b-a)

    def findFinger(self, node, key):
        current=node

        for x in node.finger.values():
            if self.distance(current.id, key.id) > self.distance(x.id, key.id):
                current = x

        return current

    def lookup(self, start, goal):
        table = []
        table.append(self.nodes[start].id)
        current=self.findFinger(self.nodes[start], self.nodes[goal])
        table.append(current.id)
        next=self.findFinger(current, self.nodes[goal])
        while self.distance(current.id, self.nodes[goal].id) > self.distance(next.id, self.nodes[goal].id):
            current=next
            next=self.findFinger(current, self.nodes[goal])
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

    def leave(self, id):
        for n in self.nodes.values():
            for succ,finger in n.finger.items():
                if finger.id == id:
                    nextFinger = next(iter(self.nodes[finger.id].finger))
                    while not nextFinger in self.nodes:
                        nextFinger = (nextFinger + 1 ) % self.size
                    n.finger[succ] = self.nodes[nextFinger]
        del self.nodes[id]

    def join(self, id):
        node = ChordNode(id,self.k,"Chord")
        # has to update itself if it joins
        for succ,finger in node.finger.items():
            nextFinger = succ
            while not nextFinger in self.nodes:
                nextFinger = ( nextFinger + 1 ) % self.size
            node.finger[succ] = self.nodes[nextFinger]
        self.nodes[id] = node 
        
        for n in self.nodes.values():
            for succ,finger in n.finger.items():
                nextFinger = succ
                while not nextFinger in self.nodes:
                    nextFinger = ( nextFinger + 1 ) % self.size
                n.finger[succ] = self.nodes[nextFinger]

def main():
    chord = Chord(4)
    nodes = chord.nodes

    table = chord.lookup(11,7)
    print(table)
    print("Hops:", len(table)-1)

    chord.leave(1)
    chord.leave(2)
    chord.leave(4)
    chord.leave(8)
    chord.leave(3)
    chord.leave(6)
    chord.leave(5)
    chord.leave(15)
    chord.leave(14)
    chord.leave(9)
    chord.leave(12)
    chord.leave(11)

    chord.join(1)
    chord.join(2)
    chord.join(4)
    chord.join(8)
    chord.join(6)
    chord.join(5)
    chord.join(15)
    chord.join(14)
    chord.join(9)
    chord.join(12)
    chord.join(11)
    #chord.join(3)

    table = chord.lookup(11,7)
    print(table)
    print("Hops:", len(table)-1)

    nodes = dict(sorted(nodes.items(), key=lambda item: item[1].id)) 
    for i in nodes.values():
        i.printTables()

if __name__ == '__main__':
    main()