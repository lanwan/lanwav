#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Steven.ZDWang
#
# Created:     25/10/2017
# Copyright:   (c) Steven.ZDWang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logging
import os

import io_config
import io_db


import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.options
from tornado import gen

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userid")

    def get_current_role_id(self):
        return self.get_secure_cookie("role_id")

class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.get_current_user():
            self.redirect('/app/main', True)
        else:
            role_id = io_db.getShareDB().verify_user( self.get_argument('userid'), self.get_argument('pwd'))
            if role_id:
                self.set_secure_cookie("role_id", role_id)
                if self.get_argument('save'):
                    self.set_secure_cookie("userid", self.get_argument("userid"))
                self.redirect('/app/main', True)
            else:
                self.redirect('/login')

    @tornado.web.authenticated
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("covguard.html", items=items)


class CoverHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("cover.html", items=items)



class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/app/main')
            return
        self.render('login.html')


class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("userid")
            self.redirect("/")

################################################################################
debug_cmds = []
class ReportHandler(BaseHandler):
    def get(self):
        global debug_cmds
        cmd = self.get_argument('DT', '')
        if len(cmd):
            debug_cmds.append(cmd)
            return self.write(cmd)
        else:
            return self.write('ERROR')


class DebugHandler(BaseHandler):
    def get(self):
        global debug_cmds
        cmd = self.get_argument('cmd', '')
        if cmd == '1':
            return self.write( ''.join(debug_cmds) )
        else:
            debug_cmds = []
            return self.write( 'clear done' )
################################################################################

class AdminHandler(BaseHandler):
    def get_login_url(self):
        return '/admin/login'


################################################################################
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        self.write_message(u"Your message was: "+message)

    def on_close(self):
        pass


################################################################################

##imei, battery bcs, battery bcl, battery vol, signal rssi, signal ber, longitude, latitude, sensor state, sensor x, sensor y, sensor z, global_count
##            self.write( json.dumps([{"id":"1211", "imei":"1212233", "vol":3.3, "rssi":18, "lon":"120.795172", "lat":"30.703541", "state":0, "x":12,"y":22,"z":98,"gct":11},
##            {"id":"1111", "imei":"1212234", "vol":3.3, "rssi":18, "lon":"120.817019", "lat":"30.734338", "state":0, "x":12,"y":22,"z":98,"gct":11}]) )


import json
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://127.0.0.1:5000")


def get_realtime_dataset(role_id):
    cmd = {}
    cmd['cmd'] = 'get_realtime_dataset'
    cmd['p1'] = role_id
    socket.send( json.dumps(cmd) )
    s = socket.recv()
    print s
    return s


class RealtimeDataHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        if self.get_current_user():
            s = yield get_realtime_dataset( self.get_current_role_id() )
            self.write( s )
        else:
            self.write('{error}')


################################################################################


# tornado global settings, such as template path, debug
import os

import io_config

def run():

    tornado.options.parse_command_line()

    settings = {
        "static_path" : os.path.join(os.path.dirname(__file__), "static"),
        "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
        "gzip" : True,
        "debug" : True,
        "xsrf_cookies" : True,
        "login_url": '/login',
        'cookie_secret' : '2bd7rtaw3i7flarndrwavytrftey6e'
    }

    application = tornado.web.Application([
        (r"/app/main", MainHandler),
        (r"/app/cover", CoverHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/report", ReportHandler),
        (r"/debug", DebugHandler),
        (r'/app/ws', WebSocketHandler),
        (r"/api/rtdata.json", RealtimeDataHandler),
        ],
        **settings)


    application.listen(io_config.settings['webport'])
    #tornado.ioloop.IOLoop.instance().add()
    tornado.ioloop.IOLoop.instance().start()

def main():
    run

if __name__ == '__main__':
    main()
