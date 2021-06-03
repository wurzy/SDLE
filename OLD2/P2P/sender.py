from P2P.Connection import Connection
import sys

destination = 'localhost'
port = 3333

con = Connection(destination, port)
con.connect()
con.send(sys.argv[1])