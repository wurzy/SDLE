import time
import socket
import configparser
import os
import argparse
import sys
import asyncio
import settings
import re
import bcrypt

from threading import Thread
from kademlia_server import KademliaServer
from node import Node
from utils.menu.menu import Menu
from utils.menu.menu_item import MenuItem

LOOP = None
NODE = None
KS = None
AUTH_MENU = None
MAIN_MENU = None
ADDRESS = None
PORT = None

async def post_message():
    global KS, NODE

    message = input("Message: ")

    try:
        state = NODE.get_state()
        followers = await KS.get_location_and_followers(state['followers'])
    except Exception as e:
        print(e)

    await NODE.post_message(message, followers)


async def follow_user():
    global LOOP, KS, NODE

    username = input("Follow user: ")

    try:
        await NODE.follow_user(username, LOOP)
    except Exception as e:
        print(e)
        return


async def unfollow_user():
    global LOOP, KS, NODE

    username = input("Unfollow user: ")

    try:
        await NODE.unfollow_user(username, LOOP)
    except Exception as e:
        print(e)
        return


def show_timeline():
    global MAIN_MENU, NODE

    NODE.show_timeline()

async def login():
    global NODE, KS

    username = input("Username: ")
    password = input("Password: ")

    try:
        state = await KS.login(username, password.encode())
        NODE = Node(address, port, username, KS, state)
        await NODE.update_timeline_messages()
        print("Login was successful")

        return 1
    except Exception as e:
        print(e)
        return 0

async def logout():
    global NODE, KS
    NODE.logout()
    KS.close_server()
    return False

async def leave():
    global KS
    KS.close_server()
    return None

async def register(address, port):
    global NODE, KS

    username = input("Username: ")
    password = input("Password: ")

    salt = bcrypt.gensalt(rounds=16)
    hash = bcrypt.hashpw(password.encode(), salt)

    try:
        state = await KS.register(username,hash)
        NODE = Node(address, port, username, KS, state)
        print("Registration was successful")

        return 1
    except Exception as e:
        print(e)
        return 0


def build_main_menu():
    menu = Menu("Timeline")
    menu.append_item(MenuItem("Show timeline", show_timeline))
    menu.append_item(MenuItem("Write a message", post_message))
    menu.append_item(MenuItem("Subscribe user", follow_user))
    menu.append_item(MenuItem("Remove subscription", unfollow_user))
    menu.append_item(MenuItem("Logout", logout))

    return menu


def build_auth_menu(address, port):
    menu = Menu("Welcome")
    menu.append_item(MenuItem("Login", login))
    menu.append_item(MenuItem("Register", register, address, port))
    menu.append_item(MenuItem("Quit", leave))

    return menu


def run_main_menu():
    global MAIN_MENU
    MAIN_MENU = build_main_menu()
    while True:
        res = MAIN_MENU.execute()
        input("Press any key to continue...")
        if res is False:
            break
    main(ADDRESS,PORT)
    
def run_auth_menu():
    global AUTH_MENU
    AUTH_MENU = build_auth_menu(address, port)
    while True:
        auth_successful = AUTH_MENU.execute()
        if auth_successful == None:
            break
        input("Press any key to continue...")
        if auth_successful == 1:
            run_main_menu()
            break


def main(address, port):
    global KS, LOOP

    bt_addresses_p = [address_port.split(":")
                      for address_port in settings.BOOTSTRAP_NODES.split(",")]
    bt_addresses = [(x, int(y)) for [x, y] in bt_addresses_p] 
    KS = KademliaServer(address, port)
    LOOP = KS.start_server(bt_addresses)

    Thread(target=LOOP.run_forever, daemon=True).start()

    run_auth_menu()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--address', type=str, help="Host IP Address",
                    default="localhost", required=True)
    ap.add_argument('-p', '--port', type=int, help="Listen port", default=2222,
                    required=True)
    args = vars(ap.parse_args())

    address = args.get("address")
    port = args.get("port")

    if not re.match(r'^(\d{1,3})(\.\d{1,3}){3}$', address) \
       and address != "localhost":
        sys.stderr.write('Address format is not valid.')
        sys.exit()

    ADDRESS = address 
    PORT = port

    main(address, port)
