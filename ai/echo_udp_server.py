import SocketServer

class EchoUDPServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print data
        socket = self.request[1]
        socket.sendto(data, self.client_address)

def run(host, port):
    server = SocketServer.UDPServer((host, port), EchoUDPServer)
    server.serve_forever()


if __name__ == '__main__':
    run('0.0.0.0', 7001)
