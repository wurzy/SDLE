import logging
import asyncio
import sys

from kademlia.network import Server

DEBUG = False 

# starting a node
def start_node(Port, BTIp="", BTPort=0): 
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # DEBUG
    if DEBUG:
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    server = Server()
    server.listen(Port)

    loop = asyncio.get_event_loop()
    if DEBUG:
        loop.set_debug(True)

    # the first peer don't do that
    if not BTPort == 0:    
        bootstrap_node = (BTIp, int(BTPort))
        loop.run_until_complete(server.bootstrap([bootstrap_node]))

    return (server, loop)