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
import urllib2
import time
server = None

import urllib
import urllib2

def httpGet(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)
        print response.read()
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason

class AiUDPServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip().replace(" ", "")
        socket = self.request[1]
        #socket.sendto(data, self.client_address)
        #rs = time.strftime("%H%M%S")
        socket.sendto('aw,120.55.61.110:9100,36,120.795172,30.703541', self.client_address)

        s = "http://120.55.61.110:8090/report?DT=%s" % (data)
        print s
        httpGet(s)


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


