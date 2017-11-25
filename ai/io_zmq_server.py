#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Steven.ZDWang
#
# Created:     17/11/2017
# Copyright:   (c) Steven.ZDWang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zmq
import time
import json


class AiZMQServer:
    def __init__(self):
        self.__realtime_ds = {}
        self.__live_users = {}


    def get_realtime_dataset(self, role_id):
        res = []
        if self.__live_users.has_key(role_id):
            stations = self.__live_users[role_id]

            for i in stations:
                res.append( self.__realtime_ds[i] )

        return res


    def add_realtime_data(self, station_id, data):
        self.__realtime_ds[station_id] = data

    def run(self):
        while True:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:5000")

            s = socket.recv()
            print s
            cmd = json.loads( s )
            if cmd['cmd'] == 'add_realtime_data':
                self.add_realtime_data(cmd['station_id'], cmd['data'])
            elif cmd['cmd'] == 'get_realtime_dataset':
                self.socket.send( self.get_realtime_dataset(cmd['role_id']) )


def main():
    server = AiZMQServer()
    server.run()

if __name__ == '__main__':
    main()
