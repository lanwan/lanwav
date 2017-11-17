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
import io_db

server = None


import json
import zmq

# <version tag>,<report number>,<imei>,<battery bcl>,<battery bcs>,<signal rssi>,<signal ber>,<sensor state>,<x hex>,<y hex>,<z hex>,<gps lon>,<gps lat>,<crc>\n
def add_realtime_data(data):
    cmd = {}
    cmd['cmd'] = 'add_realtime_data'
    cmd['station_id'] = data[2]  # station
    cmd['data'] = data
    s = json.dumps(cmd)
    print s

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://127.0.0.1:5000")
    socket.send( s )
    print "send zmq"


class AiUDPServer(SocketServer.BaseRequestHandler):

    datalist = []

    def handle(self):
        s = self.request[0].strip()
        print s
        socket = self.request[1]
        socket.sendto(s, self.client_address)

        if s.startswith('lw-'):
            data = s.split(',')
            # add data to memory server
            if len(data) > 2:
                add_realtime_data(data)


def run(host, port):
    server = SocketServer.ThreadingUDPServer( (host, port), AiUDPServer)
    server.serve_forever()


def stop():
    if server:
        server.shutdown()
        server = None

if __name__ == "__main__":
     HOST, PORT = io_config.settings['host'], io_config.settings['udp_data_port']
     run(HOST,PORT)


