import pymongo
from datetime import datetime

class MongoController:

    def __init__(self, user):
        self.conn = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.conn["SDLE"]
        self.timeline = self.db[user + "_timeline"]
        self.queue = self.db[user + "_queue"]
        self.user = user

    def saveMessage(self,user,msg):
        if not self.timeline.count_documents({ 'user': user }, limit = 1):
            self.timeline.insert_one({'user': user, 'messages': []})
        self.timeline.update({'user': user}, { "$push": { "messages": msg } })

    def saveMessageInQueue(self,user,msg):
        if not self.queue.count_documents({ 'user': user }, limit = 1):
            self.queue.insert_one({'user': user, 'messages': []})
        self.queue.update({'user': user}, { "$push": { "messages": msg } })

    def saveMessages(self, timeline:dict):
        for user,msgs in timeline.items():
            for msg in msgs.values():
                self.saveMessage(user,msg)

    def saveQueue(self, queue:dict):
        for user,msgs in queue.items():
            for msg in msgs.values():
                self.saveMessageInQueue(user,msg)

    def getTimeline(self):
        try:
            messages = {}
            for user_msgs in self.timeline.find():
                user = user_msgs['user']
                messages[user] = {}
                for msg in user_msgs['messages']:
                    msg['time'] = datetime.strptime(str(msg['time']),'%Y-%m-%d %H:%M:%S.%f')
                    msg_nr = msg['msg_nr']
                    messages[user][str(msg_nr)] = msg
        except Exception as e:
            print("Error mongoDB Timeline: ", e) 
            messages = {}    
        finally:
            return messages
    
    def getQueue(self):
        try:
            messages = {}
            for user_msgs in self.queue.find():
                user = user_msgs['user']
                messages[user] = {}
                for msg in user_msgs['messages']:
                    msg['time'] = datetime.strptime(str(msg['time']),'%Y-%m-%d %H:%M:%S.%f')
                    msg_nr = msg['msg_nr']
                    messages[user][str(msg_nr)] = msg
        except Exception as e:
            print("Error mongoDB Queue: ", e) 
            messages = {}    
        finally:
            return messages

    def dropCollections(self):
        self.timeline.drop()
        self.queue.drop()