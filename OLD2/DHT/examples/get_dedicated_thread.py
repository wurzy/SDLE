import logging
import asyncio
import sys

from kademlia.network import Server

from threading import Thread
from time import sleep

def readingStdinThread(loop, server):
    print("Welcome")
    while True:
        msg = input('> ')
        print(msg)
        # loop.create_task(server.set('key', msg))
        asyncio.ensure_future(server.set('key', msg), loop=loop)

def start_node(BTIp, BTPort, Port): # starting a node
   handler = logging.StreamHandler()
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setFormatter(formatter)
   log = logging.getLogger('kademlia')
   log.addHandler(handler)
   log.setLevel(logging.DEBUG)

   server = Server()
   server.listen(Port)

   loop = asyncio.get_event_loop()
   loop.set_debug(True)

   bootstrap_node = (BTIp, int(BTPort))
   loop.run_until_complete(server.bootstrap([bootstrap_node]))

   return (server, loop)

if __name__ == "__main__":
    (server, loop) = start_node(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    thread = Thread(target = readingStdinThread, args = (loop, server, ))
    thread.start()
    loop.run_forever()
    #thread.join()
    server.stop()
    loop.close()