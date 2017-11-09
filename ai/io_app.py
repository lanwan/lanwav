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

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userid")

class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.get_current_user():
            self.redirect('/app/main', True)
        else:
            r = io_db.dbserver.verify( self.get_argument('userid'), self.get_argument('pwd'))
            if r:
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

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        self.write_message(u"Your message was: "+message)

    def on_close(self):
        pass


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
        ],
        **settings)


    application.listen(io_config.settings['webport'])
    #tornado.ioloop.IOLoop.instance().add()
    tornado.ioloop.IOLoop.instance().start()

def main():
    run

if __name__ == '__main__':
    main()
