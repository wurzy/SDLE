from timeline.timeline import *

class Node:
    def __init__(self, ID, nxt = None, prev = None):
        self.ID = ID
        self.data = dict()
        self.prev = prev
        self.fingerTable = [nxt]
        self.timeline = Timeline()

    # Update the finger table of this node when necessary
    def updateFingerTable(self, dht, k):
        del self.fingerTable[1:]
        for i in range(1, k):
            self.fingerTable.append(dht.findNode(dht._startNode, self.ID + 2 ** i))
            
    def getFingerTable(self):
        return [x.ID for x in self.fingerTable]
    
    def addToTimeline(self,post):
        self.timeline.add(post)