import hashlib
import random
from math import log2

from .kbucket import KBucket

def xor(b1, b2):
    assert len(b1) == len(b2)
    i1 = int.from_bytes(b1, 'big')
    i2 = int.from_bytes(b2, 'big')

    return i1 ^ i2

class NodeK:
    def __init__(self, k):
       self._id =  hashlib.sha256(str(random.randint(0, 2**32 - 1)).encode('utf-8')).hexdigest()[:20]
       self._kbucket = KBucket(k)

    def getid(self):
        return self._id

    def find_node(self, nodeid):
        distance = xor(self._id.encode('utf-8'), nodeid.encode('utf-8'))
        return self._kbucket.getkclose(distance)

    def addcontact(self, contact):
        contactId = contact[0]

        distance = xor(self._id.encode('utf-8'), contactId.encode('utf-8'))
        if(log2(distance).__round__() - 1  <= log2(distance)):
            index = log2(distance).__round__() - 1
        else:
            index = log2(distance).__round__()
        self._kbucket.add(contact, index)