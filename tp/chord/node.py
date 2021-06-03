from timeline.timeline import *
from timeline.post import *
from .chord import *

class Node:
    def __init__(self, ID, nxt = None, prev = None):
        self.ID = ID
        self.data = dict()
        self.prev = prev
        self.fingerTable = [nxt]
        self.timeline = []
        self.subscribers = []

    # Update the finger table of this node when necessary
    def updateFingerTable(self, dht, k):
        del self.fingerTable[1:]
        for i in range(1, k):
            self.fingerTable.append(dht.findNode(dht._startNode, self.ID + 2 ** i))
            
    def getFingerTable(self):
        return [x.ID for x in self.fingerTable]

    def registerSub(self, key):
        print(f"Node {key} subscribed to node {self.ID}.")
        self.subscribers.append(key)

    def unregisterSub(self, key):
        self.subscribers.remove(key)
    
    def addToTimeline(self, post):
        self.timeline.append(post)

        if (self.ID == 11):
            print("TIMELINE (node 11) ----------------------")
            for post in self.timeline:
                print(f"Node {post.user}: ...")
            print()