from networking.server.server import Server

host = 'localhost'
port = 5555

server = Server(host, port, False)
server.start()
