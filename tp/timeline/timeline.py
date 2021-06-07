import threading
import settings

from datetime import datetime, timedelta
from mongo.connection import MongoController

DISCARD_BASELINE = settings.DISCARD_BASELINE


class TimelineEntry:
    def __init__(self, username, content, msg_nr, time):
        self.username = username
        self.content = content
        self.msg_nr = msg_nr
        self.time = time
        self.seen = False

    def get_dict(self):
        return {
            "username": self.username,
            "message": self.content,
            "msg_nr": self.msg_nr,
            "time": self.time,
            "seen": self.seen
        }


class Timeline:
    def __init__(self, username):
        self.username = username
        self.lock = threading.RLock()
        self.mongo = MongoController(username)
        self.get_timeline()

    def __repr__(self):

        messages = []
        for msgs in self.messages.values():
            for msg in msgs.values():
                msg['seen'] = True
                messages.append(msg)

        self.save_messages()

        messages = sorted(messages, key=lambda x: str(x['time']), reverse=True)

        result = ""

        for msg in messages:
            time = datetime.strptime(str(msg['time']),'%Y-%m-%d %H:%M:%S.%f')

            result += "-" * 79 + "\n"
            result += time.strftime('%Y-%m-%d %H:%M:%S') + " - "
            result += msg.get("username") + ": " + msg.get("message")
            result += "\n"

        return self.username + "'s TIMELINE" + "\n" + result

    def get_user_messages(self, user, msgs_idx):

        msgs = []
        for msg_idx in msgs_idx:
            if msg_idx in self.messages[user]:
                msg = self.messages[user][msg_idx]
                msgs.append({
                    "username": msg['username'],
                    "message": msg['message'],
                    "msg_nr": msg['msg_nr'],
                    "time": msg['time']
                })

        return msgs

    def discard_messages(self):
        max_duration = timedelta(seconds=DISCARD_BASELINE)

        discard_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f") - max_duration

        self.lock.acquire()

        messages = dict(self.messages)

        for user, msgs in self.messages.items():
            user_msgs = dict(msgs)

            for msg_nr, msg in msgs.items():
                if datetime.strptime(str(msg['time']), "%Y-%m-%d %H:%M:%S.%f") < discard_time and msg['seen']:
                    user_msgs.pop(msg_nr)
                else:
                    break
            messages[user] = user_msgs
        self.messages = messages
        self.lock.release()

    def user_waiting_messages(self, follw):
        if follw in self.waiting_messages:
            return list(self.waiting_messages[follw].keys())
        else:
            return []

    def add_message(self, user, message, msg_nr, time,
                    user_knowledge=None):

        timeline_entry = TimelineEntry(user, message, msg_nr, time)

        self.lock.acquire()

        user_knowledge_inc = ""

        if (user_knowledge is not None):
            user_knowledge_split = user_knowledge.split('-')
            user_knowledge_split[len(user_knowledge_split)-1] = str(int(user_knowledge_split[len(user_knowledge_split)-1])+1)
            user_knowledge_inc = '-'.join(user_knowledge_split)

        if (user_knowledge is None) or (msg_nr == user_knowledge_inc):
            user_msgs = self.messages.get(user, {})
            user_msgs[msg_nr] = (timeline_entry.get_dict())
            user_knowledge = msg_nr

            while(user_knowledge in self.waiting_messages):
                msg = self.waiting_messages.pop(user_knowledge)
                user_msgs[user_knowledge] = msg

                user_knowledge_split = user_knowledge.split('-')
                user_knowledge_split[len(user_knowledge_split)-1] = str(int(user_knowledge_split[len(user_knowledge_split)-1])+1)
                user_knowledge = '-'.join(user_knowledge_split)

            self.messages[user] = user_msgs

        elif msg_nr > user_knowledge_inc:
            user_msgs = self.waiting_messages.get(user, {})
            user_msgs[msg_nr] = (timeline_entry.get_dict())
            self.waiting_messages[user] = user_msgs
        else:
            pass
        self.lock.release()

        self.discard_messages()
        self.save_messages()

    def get_timeline(self):
        self.messages = self.mongo.getTimeline()
        self.waiting_messages = self.mongo.getQueue()

    def save_messages(self):
        self.mongo.dropCollections()
        self.save_current_messages()
        self.save_waiting_messages()

    def save_current_messages(self):
        messages = {}
        self.lock.acquire()
        for user, msgs in self.messages.items():
            user_msgs = {}
            for msg_nr, msg in msgs.items():
                new_msg = dict(msg)
                new_msg['time'] = datetime.strptime(str(new_msg['time']), "%Y-%m-%d %H:%M:%S.%f")
                user_msgs[msg_nr] = new_msg
            messages[user] = user_msgs
        self.mongo.saveMessages(messages)
        self.lock.release()

    def save_waiting_messages(self):
        messages = {}
        self.lock.acquire()
        for user, msgs in self.waiting_messages.items():
            user_msgs = {}
            for msg_nr, msg in msgs.items():
                new_msg = dict(msg)
                new_msg['time'] = datetime.strptime(str(new_msg['time']), "%Y-%m-%d %H:%M:%S.%f")
                user_msgs[msg_nr] = new_msg
            messages[user] = user_msgs
        self.mongo.saveQueue(messages)
        self.lock.release()
