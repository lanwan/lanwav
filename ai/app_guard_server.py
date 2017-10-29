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

try:
    import tornado
    import tornado.ioloop
    import tornado.web
except:
    logging.error('Load tornado library fail!')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("covguard.html", items=items)


class CoverHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("cover.html", items=items)


# tornado global settings, such as template path, debug
import os

settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "gzip" : True,
    "debug" : False,
    "xsrf_cookies" : True,
}

import io_config

def run():
    application = tornado.web.Application([
        (r"/app", MainHandler),
        (r"/app/cover", CoverHandler),
        ],
        **settings)
    application.listen(io_config.settings['webport'])
    tornado.ioloop.IOLoop.instance().start()

def main():
    run

if __name__ == '__main__':
    main()
