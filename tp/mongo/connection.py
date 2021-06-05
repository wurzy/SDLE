import pymongo

class MongoController:

    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.conn["SDLE"]
        self.timeline = self.db["timeline"]
        self.queue = self.db["queue"]

    def saveMessage(self,msg,user):
        self.timeline.insert_one(msg)

    def saveMessageInQueue(self,msg):
        self.queue.insert_one(msg)
