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
import urllib

server = None

class AiUDPServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(data, self.client_address)
        urllib.urlopen("http://120.55.61.110:8090/report?DT=", data)


def run(host, port):
    server = SocketServer.UDPServer((host, port), AiUDPServer)
    server.serve_forever()


def stop():
    if server:
        server.shutdown()
        server = None

if __name__ == "__main__":
     HOST, PORT = io_config.settings['host'], io_config.settings['udp_echo_port']
     run(HOST,PORT)


