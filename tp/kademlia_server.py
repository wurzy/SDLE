import logging
import asyncio
import sys
import json
import bcrypt

from threading import *
from kademlia.network import Server

DEBUG = False


class KademliaServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = None

    def start_server(self, bootstrap_nodes):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      '- %(message)s')
        handler.setFormatter(formatter)

        # DEBUG
        if DEBUG:
            log = logging.getLogger('kademlia')
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)

        self.loop = asyncio.get_event_loop()
        if DEBUG:
            self.loop.set_debug(True)

        self.server = Server()
        self.loop.run_until_complete(self.server.listen(self.port))
        self.loop.run_until_complete(self.server.bootstrap(bootstrap_nodes))

        return self.loop

    def close_server(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.server.stop()

    async def register(self, username, password):
        result = await self.server.get(username)
        if result is None:
            value = {
                "password": password.decode(),
                "followers": [],
                "following": {username: (0, 0)},
                "redirect": {},
                "ip": self.ip,
                "port": self.port
            }
            value_to_set = json.dumps(value)
            await self.server.set(username, value_to_set)
            return value

        else:
            raise Exception("Username already exists")

    async def login(self, username, password):
        result = await self.server.get(username)
        result = json.loads(result)

        if result is not None:
            encoded = result['password'].encode()

            if not bcrypt.checkpw(password,encoded):
                raise Exception("Incorrect credentials, try again")

            value = {
                "password": result['password'],
                "followers": result['followers'],
                "following": result['following'],
                "redirect": result['redirect'],
                "ip": self.ip,
                "port": self.port
            }
            value_to_set = json.dumps(value)
            await self.server.set(username, value_to_set)
            return value

        else:
            raise Exception("Invalid user, register first")

    async def get_user_ip(self, username):
        result = await self.server.get(username)
        result = json.loads(result)

        if result is None:
            raise Exception("Invalid user")
        else:
            return (result["ip"], result["port"])

    async def get_user_ip_msgnr(self, username):
        result = await self.server.get(username)
        result = json.loads(result)

        if result is None:
            raise Exception("Invalid user")
        else:
            return (result["ip"], result["port"], result["following"][username][0])

    async def get_location_and_followers(self, usernames):
        res = {}
        for username in usernames:
            result = await self.server.get(username)
            result = json.loads(result)

            if result is not None:
                res[username] = (result["ip"],
                                 result["port"],
                                 result["followers"])

        return res

    async def get_user_followers(self, username):
        followers = {}

        result = await self.get_user(username)

        for follower in result["followers"]:
            result = await self.server.get(follower)
            result = json.loads(result)

            if result is not None:
                followers[follower] = (result["ip"],
                                       result["port"],
                                       result["followers"])

        return followers

    async def get_users_following_user(self, user):
        user = await self.get_user(user)
        user_followers = user['followers']
        return user_followers

    async def get_outdated_user_following(self, following):
        res = []

        for follw, info in following.items():

            user_knowledge = info[0]
            result = await self.server.get(follw)
            result = json.loads(result)
            msg_nr = result["following"][follw][0]
            if (result is not None) and msg_nr > user_knowledge:
                res.append((follw, result["ip"], result["port"], msg_nr))

        return res

    """ async def get_user_following(self, state):
        following = {}

        result = await self.get_user(username)

        for follw in result["following"]:
            result = await self.server.get(follw)
            result = json.loads(result)
            if result is not None:
                following[follw] = (result["ip"],
                                    result["port"])

        return following """

    async def get_user(self, username):
        result = await self.server.get(username)
        result = json.loads(result)
        return result

    async def set_user(self, username, value):
        await self.server.set(username, value)
