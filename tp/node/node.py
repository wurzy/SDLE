import asyncio
import json
import settings

from datetime import datetime
from random import choices
from threading import Thread
from timeline.timeline import Timeline

KS = None
LOOP = None
USERNAME = None
STATE = None
LIST_LOOP = None
TIMELINE = None
NODE = None
FOLLOWERS_CONS = None

async def send_message_to_user(user, ip, port, message,
                               established_connections):
    res = True
    try:
        try:
            established_connections[user] = await asyncio.open_connection(
                ip, port, loop=asyncio.get_event_loop())

            established_connections[user][1].write(message.encode())
            await established_connections[user][1].drain()
        except ConnectionResetError:
            established_connections[user] = await asyncio.open_connection(
                            ip,
                            port,
                            loop=asyncio.get_event_loop())

            established_connections[user][1].write(message.encode())
            await established_connections[user][1].drain()
        except Exception as e:
            pass
    except Exception as e:
        print(e)
        res = False

    return res

async def send_message_to_users(users, message, established_connections):
    usernames = list(users.keys())
    tasks = [send_message_to_user(user, users[user][0], users[user][1],
             message, established_connections) for user in usernames]
    finished = await asyncio.gather(*tasks)

    true_users = []
    false_users = []
    for i in range(len(finished)):
        if finished[i] is True:
            true_users.append(usernames[i])
        else:
            false_users.append(usernames[i])
    return true_users, false_users


async def node_server(reader, writer):
    global LIST_LOOP, TIMELINE, KS, STATE, FOLLOWERS_CONS, LOOP

    while True:
        data = (await reader.readline()).strip()

        if not data:
            break

        json_string = data.decode()
        data = json.loads(json_string)

        if "follow" in data:
            new_follower = data["follow"]["username"]

            if new_follower in STATE['followers']:
                writer.write(b'0\n')
                await writer.drain()
            else:
                STATE["followers"].append(new_follower)
                value = json.dumps(STATE)

                future = asyncio.run_coroutine_threadsafe(
                                 KS.set_user(USERNAME, value),
                                 LOOP)
                future.result()
                writer.write(b'1\n')
                await writer.drain()

        elif 'unfollow' in data:
            unfollower = data["unfollow"]["username"]

            if unfollower not in STATE['followers']:
                writer.write(b'0\n')
                await writer.drain()
            else:
                STATE["followers"].remove(unfollower)
                value = json.dumps(STATE)

                future = asyncio.run_coroutine_threadsafe(
                                 KS.set_user(USERNAME, value),
                                 LOOP)
                future.result()
                writer.write(b'1\n')
                await writer.drain()

        elif 'post' in data:
            sender = data["post"]["username"]
            message = data["post"]["message"]
            msg_nr = data["post"]["msg_nr"]
            time = data["post"]["time"]
            user_knowledge = STATE["following"][sender][0]
            
            TIMELINE.add_message(sender, message, msg_nr, time, user_knowledge)

            user_knowledge_split = user_knowledge.split('-')
            user_knowledge_split[-1] = str(int(user_knowledge_split[len(user_knowledge_split)-1])+1)
            user_knowledge_inc = '-'.join(user_knowledge_split)

            if (user_knowledge is None or msg_nr == user_knowledge_inc):
                STATE["following"][sender] = (msg_nr, time)
                value = json.dumps(STATE)
                future = asyncio.run_coroutine_threadsafe(
                                    KS.set_user(USERNAME, value),
                                    LOOP)
                future.result()
            elif msg_nr > user_knowledge_inc:
                waiting_msgs = TIMELINE.user_waiting_messages(sender)
                wanted_msgs = []

                username = '-'.join(msg_nr.split('-').pop())
                user_knowledge_nr = int(user_knowledge.split('-')[-1])
                msg_nr_nr = int(msg_nr.split('-')[-1])

                for nr in range(user_knowledge_nr + 1, msg_nr_nr):
                    nr_complete = username + '-' + str(nr)

                    if nr_complete not in waiting_msgs:
                        wanted_msgs.append(nr_complete)

                    messages = await request_messages(sender,
                                                      wanted_msgs,
                                                      reader=reader,
                                                      writer=writer)
                    if messages != []:
                        await handle_messages(messages, thread_safe=True)

        elif 'online' in data:
            username = data['online']['username']
            NODE.add_follower_connection(username, reader, writer)

        elif 'msgs_request' in data:

            user = data["msgs_request"]["username"]
            messages_ids = data["msgs_request"]["messages"]
            messages = TIMELINE.get_user_messages(user, messages_ids)

            data = {
                "messages": messages
            }

            json_string = json.dumps(data) + '\n'
            writer.write(json_string.encode())
            await writer.drain()

    writer.close()


class Listener(Thread):

    def __init__(self, address, port):
        super(Listener, self).__init__()
        self.address = address
        self.port = port
        self.server = None

    def close_listener(self):
        self.server.close()

    async def start_listener(self):
        self.server = await asyncio.start_server(node_server,
                                                 self.address,
                                                 self.port)

        await self.server.serve_forever()

    def run(self):
        global LIST_LOOP
        LIST_LOOP = asyncio.new_event_loop()
        try:
            result = LIST_LOOP.run_until_complete(self.start_listener())
        except Exception:
            pass


class Node:
    def __init__(self, address, port, username, ks, state):
        global KS, LOOP, USERNAME, TIMELINE, NODE, STATE
        global FOLLOWERS_CONS

        TIMELINE = Timeline(username)
        USERNAME = username
        STATE = state
        KS = ks
        LOOP = asyncio.get_event_loop()
        self.address = address
        self.port = port
        FOLLOWERS_CONS = {}

        self.following_cons = {}
        self.listener = Listener(self.address, self.port)
        self.listener.daemon = True
        self.listener.start()

    def get_username(self):
        global USERNAME

        return USERNAME

    def get_state(self):
        global STATE

        return STATE

    async def post_message(self, message, followers):
        global USERNAME, TIMELINE, STATE, FOLLOWERS_CONS

        msg_nr_split = STATE['following'][USERNAME][0].split("-")
        msg_nr_split[-1] = str(int(msg_nr_split[-1])+1)
        msg_nr = '-'.join(msg_nr_split)

        time = str(datetime.now())

        STATE['following'][USERNAME] = (msg_nr, time)

        # Add to timeline
        TIMELINE.add_message(USERNAME, message, msg_nr, time)

        data = {
            "post": {
                "username": USERNAME,
                "message": message,
                "msg_nr": msg_nr,
                "time": time
            }
        }

        json_string = json.dumps(data) + '\n'

        await send_message_to_users(followers, json_string, FOLLOWERS_CONS)

        value = json.dumps(STATE)

        await KS.set_user(USERNAME, value)

    async def update_timeline_messages(self):

        outdated_follw = await KS.get_outdated_user_following(
                                  STATE["following"])

        for (follw, ip, port, user_knowledge) in outdated_follw:
            current_knowledge = STATE["following"][follw][0]

            waiting_msgs = TIMELINE.user_waiting_messages(follw)
            wanted_msgs = []

            username = '-'.join(current_knowledge.split('-').pop())
            current_knowledge_nr = int(current_knowledge.split('-')[-1])
            user_knowledge_nr = int(user_knowledge.split('-')[-1])

            for msg_nr in range(current_knowledge_nr + 1, user_knowledge_nr + 1):
                msg_nr_complete = username + '-' + str(msg_nr)

                if msg_nr_complete not in waiting_msgs:
                    wanted_msgs.append(msg_nr_complete)

            try:
                messages = await request_messages(follw, wanted_msgs, ip=ip,
                                                  port=port)
                if messages != []:
                    await handle_messages(messages)
            except ConnectionRefusedError:
                user_followers = await KS.get_users_following_user(follw)
                for user in user_followers:
                    current_knowledge = STATE["following"][follw][0]
                    if (current_knowledge < user_knowledge):
                        info = await KS.get_user(user)
                        if info['following'][follw][0] > current_knowledge:
                            try:
                                messages = await request_messages(
                                    follw, wanted_msgs, ip=info['ip'],
                                    port=info['port'])
                                if messages != []:
                                    await handle_messages(messages)
                                for msg in messages:
                                    wanted_msgs.remove(msg['msg_nr'])

                            except ConnectionRefusedError:
                                continue
                        else:
                            continue
                    else:
                        break

    def logout(self):
        self.listener.close_listener()

    def show_timeline(self):
        global TIMELINE
        print(TIMELINE)

    async def follow_user(self, to_follow, loop):
        global USERNAME, STATE

        (ip, port, msg_nr) = await KS.get_user_ip_msgnr(to_follow)

        if to_follow == USERNAME:
            print("You can't follow yourself!")
            return

        elif to_follow in STATE["following"]:
            print("You already follow that user!!")

        try:
            (reader, writer) = await asyncio.open_connection(
                               ip, port, loop=loop)
        except Exception:
            print("It's not possible to follow that user right now!"
                  "(user offline)")
            return

        data = {
            "follow": {
                "username": USERNAME
            }
        }

        json_string = json.dumps(data) + '\n'
        writer.write(json_string.encode())
        await writer.drain()

        data = (await reader.readline()).strip()

        writer.close()

        if data.decode() == '1':
            print("You followed %s successfully" % to_follow)

            STATE["following"][to_follow] = (msg_nr, str(datetime.now()))
            value = json.dumps(STATE)

            await KS.set_user(USERNAME, value)

        else:
            print("It's not possible to follow %s (already followed)"
                  % to_follow)

    async def unfollow_user(self, to_unfollow, loop):
        global USERNAME, STATE

        (ip, port, msg_nr) = await KS.get_user_ip_msgnr(to_unfollow)

        if to_unfollow == USERNAME:
            print("You can't unfollow yourself!")
            return

        elif to_unfollow not in STATE["following"]:
            print("You already don't follow that user!!") 

        try:
            (reader, writer) = await asyncio.open_connection(
                               ip, port, loop=loop)
        except Exception:
            print("It's not possible to unfollow that user right now!"
                  "(user offline)")
            return

        data = {
            "unfollow": {
                "username": USERNAME
            }
        }

        json_string = json.dumps(data) + '\n'
        writer.write(json_string.encode())
        await writer.drain()

        data = (await reader.readline()).strip()

        writer.close()

        if data.decode() == '1':
            print("You unfollowed %s successfully" % to_unfollow)

            del STATE["following"][to_unfollow]
            value = json.dumps(STATE)

            await KS.set_user(USERNAME, value)

        else:
            print("It's not possible to unfollow %s (already not followed)"
                  % to_unfollow)

async def handle_messages(messages, thread_safe=False):

    for msg in messages:
        sender = msg["username"]
        message = msg["message"]
        msg_nr = msg["msg_nr"]
        time = msg["time"]
        TIMELINE.add_message(sender, message, msg_nr, time)

        user_knowledge = STATE["following"][sender][0]
        user_knowledge_split = user_knowledge.split('-')
        user_knowledge_split[-1] = str(int(user_knowledge_split[-1])+1)
        user_knowledge_inc = '-'.join(user_knowledge_split)

        if user_knowledge is None or msg_nr == user_knowledge_inc:
            STATE["following"][sender] = (msg_nr, time)

    value = json.dumps(STATE)
    await KS.set_user(USERNAME, value)

async def request_messages(user, wanted_msgs, ip=None, port=None,
                           reader=None, writer=None):
    if reader is None and writer is None:
        (reader, writer) = await asyncio.open_connection(ip, port, loop=LOOP)

    data = {
        "msgs_request": {
            "username": user,
            "messages": wanted_msgs
        }
    }

    json_string = json.dumps(data) + '\n'
    writer.write(json_string.encode())
    await writer.drain()

    data = (await reader.readline()).strip()
    writer.close()

    json_string = data.decode()
    data = json.loads(json_string)

    return data["messages"]
