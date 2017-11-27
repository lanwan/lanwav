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

import redis

__pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
__r = redis.Redis(connection_pool=pool)

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

def get_cmd_list(imei):
    cmd = {}
    cmd['cmd'] = 'get_cmd_list'
    cmd['imei'] = imei  # station
    cmd['data'] = data
    s = json.dumps(cmd)
    print s

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://127.0.0.1:5000")
    socket.send( s )
    print "send zmq"

import time


class AiUDPServer(SocketServer.BaseRequestHandler):

    datalist = []

    def handle(self):
        s = self.request[0].strip()
        print s
        socket = self.request[1]


        if s.startswith('lw-'):
            data = s.split(',')
            version_tag = data[0]
            report_numb = data[1]
            imei = data[2]
            if version_tag == 'lw-0':
                bcl = data[3]
                rssi = data[4]
                state = data[5]
                g_x = data[6]
                g_y = data[7]
                g_z = data[8]
                crc = data[9]
            if version_tag == 'lw-1':
                bcs = data[9]
                ber = data[10]
                gps_lon = data[11]
                gps_lat = data[12]
                crs = data[13]

            # add data to memory server
            if len(data) > 2:
                add_realtime_data(data)

                if not get_cmd_list(imei):
                    rs = time.strftime("lw,0,%Y%m%d%H%M%S")
                    socket.sendto(rs, self.client_address)
                else:
                    rs = time.strftime("lw,1,%Y%m%d%H%M%S")
                    socket.sendto(rs, self.client_address)


        elif s.startswith('lw,88,'):
            data = s.split(',')



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


