import asyncio, json, socket
from P2P.Connection import Connection

# process all messages into the Queue
@asyncio.coroutine
def task(server, loop, nickname, menu, queue):
    menu.draw()
    while True:
        msg = yield from queue.get()
        if not msg == '\n' and menu.run(int(msg)):
            break
        menu.draw()
    loop.call_soon_threadsafe(loop.stop)


async def task_follow(user_id, nickname, server, following, ip_address, p2p_port, vector_clock):
    result = await server.get(user_id)

    if result is None:
        print('That user doesn\'t exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][nickname]:
                print('You\'re following him!')
        except Exception:
            print('Following ' + user_id)
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][nickname] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][nickname] = 0
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))


# get followers port's
async def get_followers_p2p(server, nickname, vector_clock):
    connection_info = []
    result = await server.get(nickname)

    if result is None:
        print('ERROR - Why don\'t I belong to the DHT?')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        userInfo['vector_clock'][nickname] += 1
        vector_clock[nickname] += 1
        asyncio.ensure_future(server.set(nickname, json.dumps(userInfo)))
        for user, info in userInfo['followers'].items():
            connection_info.append(info)
    return connection_info


async def task_send_msg(msg, server, nickname, vector_clock):
    connection_info = await get_followers_p2p(server, nickname, vector_clock)
    # print('CONNECTION INFO (Ip, Port)')
    for follower in connection_info:
        #print(follower)
        info = follower.split()
        send_p2p_msg(info[0], int(info[1]), msg)


def send_p2p_msg(ip, port, message, timeline=None):
    if isOnline(ip, port):
        connection = Connection(ip, port)
        connection.connect()
        connection.send(message, timeline)


# check if a node is online
def isOnline(userIP, userPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((userIP, userPort))
    if result == 0:
        print("IS ONLINE " + userIP)
        return True
    else:
        print("NOT ONLINE " + userIP)
        return False
