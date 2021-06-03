import logging
import asyncio
import sys

from kademlia.network import Server

queue = asyncio.Queue()

def handle_stdin():
    data = sys.stdin.readline()
    asyncio.async(queue.put(data)) # Queue.put is a coroutine, so you can't call it directly.

@asyncio.coroutine
def task(server, loop):
    while True:
        msg = yield from queue.get()
        print(msg)
        asyncio.ensure_future(server.set('key',msg))

def start_node(BTIp, BTPort, Port): # starting a node
   handler = logging.StreamHandler()
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setFormatter(formatter)
   #log = logging.getLogger('kademlia')
   #log.addHandler(handler)
   #log.setLevel(logging.DEBUG)

   server = Server()
   server.listen(Port)

   loop = asyncio.get_event_loop()
   loop.set_debug(True)

   bootstrap_node = (BTIp, int(BTPort))
   loop.run_until_complete(server.bootstrap([bootstrap_node]))

   return (server, loop)

if __name__ == "__main__":
    (server, loop) = start_node(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    try:
        print('loop.run')
        loop.add_reader(sys.stdin, handle_stdin)
        asyncio.async(task(server, loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('loop.close()')
        server.stop()
        loop.close()