import logging
import asyncio
import sys
import socket
import json
from threading import Thread

from async_tasks import task, task_follow, task_send_msg, get_followers_p2p
from LocalStorage import local_storage
from DHT import node
from P2P.Connection import Connection
from Menu.Menu import Menu
from Menu.Item import Item

# build the Menu
def build_menu():
    menu = Menu('Menu')
    menu.add_item(Item('1 - Show timeline', show_timeline))
    menu.add_item(Item('2 - Follow username', follow_user))
    menu.add_item(Item('3 - Send message', send_msg))
    menu.add_item(Item('0 - Exit', exit_loop))
    return menu


# get the nickname
def get_nickname():
    nick = input('Nickname: ')
    return nick.replace('\n', '')


# follow a user. After, he can be found in the list "following"
def follow_user():
    user = input('User Nickname: ')
    user_id = user.replace('\n', '')
    asyncio.async(task_follow(user_id))
    return False


# show own timeline 
def show_timeline():
    for m in messages:
        print(m['id'] + ' - ' + m['message'])
    return False   


# send message to the followers
def send_msg():
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    print(msg)
    asyncio.async(task_send_msg(msg))
    return False 


# exit app 
def exit_loop():
    return True
