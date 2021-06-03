from P2P.Connection import Connection

host = 'localhost'
port = 3333

con = Connection(host, port)
con.bind()
con.listen()

