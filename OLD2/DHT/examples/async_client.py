import asyncio

async def tcp_echo_client(loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    while True:
        message = input('> ')
        if message == '':
            writer.close()
        else:
            print('Send: %r' % message)
            writer.write(message.encode())

    #data = await reader.read(100)
    #print('Received: %r' % data.decode())

message = 'Hello World!'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()