#-------------------------------------------------------------------------------
# Name:        io_udp_server.py
# Purpose:
#
# Author:      Steven.ZDWang
#
# Created:     23/10/2017
# Copyright:   (c) Http://www.lanwav.com 2017
# Licence:
#-------------------------------------------------------------------------------

import SocketServer
import logging
import io_config

server = None

class AiUDPServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print data
        socket = self.request[1]
        socket.sendto(data, self.client_address)

def run(host, port):
    server = SocketServer.UDPServer((host, port), AiUDPServer)
    server.serve_forever()


def stop():
    if server:
        server.shutdown()
        server = None

if __name__ == "__main__":
     HOST, PORT = io_config.settings['host'], io_config.settings['port']
     run(HOST,PORT)


