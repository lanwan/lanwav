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

class AiUDPServer(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(data.upper(), self.client_address)

def run_udp_server(host, port):
    server = SocketServer.UDPServer((host, port), AiUDPServer)
    server.serve_forever()

if __name__ == "__main__":
     HOST, PORT = io_config.io_setttins['host'], io_config.io_setttins['port']
     run_udp_server(HOST,PORT)


