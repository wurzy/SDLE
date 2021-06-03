class LinkedNode:
    def __init__(self, id, k):
        self.id = id
        self.type = type
        self.k = k
        self.size = 2**k
        self.next = None
        self.prev = None
        self.data = {}

    def successor(self, node):
        self.next = node

    def previous(self, node):
        self.prev = node

class Linked: 
    def __init__(self,k):
        self.k = k
        self.size = 2**k
        self.nodes = {}
        for i in range(2**k):
            self.nodes[i] = LinkedNode(i,k)
        
        for i in range(2**k):
            self.nodes[i].successor(self.nodes[ (i + 1) % self.size ])
            self.nodes[i].previous(self.nodes[ (i - 1) % self.size ])

    def lookup(self, start:int, goal):
        table = []
        table.append(self.nodes[start].id)
        current = self.nodes[start].next

        while current.id != goal:
            table.append(current.id)
            current = current.next
        
        table.append(goal)
        return table

    def leave(self, id):
        curr = self.nodes[id]
        prev = curr.prev
        next = curr.next
        
        prev.next = next 
        next.prev = prev

        del self.nodes[id]

    def join(self, id):
        node = LinkedNode(id,self.k)
        nextNode = ( id + 1 ) % self.size

        while not nextNode in self.nodes:
            nextNode = ( nextNode + 1 ) % self.size
        nextNode = self.nodes[nextNode]

        node.next = nextNode
        node.prev = nextNode.prev
        nextNode.prev.next = node

        self.nodes[id] = node

def main():
    linked = Linked(4)

    table = linked.lookup(11,7)
    print(table)
    print("Hops:", len(table)-1)

    linked.leave(3)
    linked.leave(0)
    linked.leave(6)

    linked.join(0)

    table = linked.lookup(11,7)
    print(table)
    print("Hops:", len(table)-1)

if __name__ == '__main__':
    main()