#-------------------------------------------------------------------------------
# Name:        io_boot.py
# Purpose:     Boot IOT AI Server
#
# Author:      Steven.ZDWang
#
# Created:     24/10/2017
# Copyright:   (c) Steven.ZDWang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os


print "boot covguard server ..."

# setup logger
import logging
from logging.handlers import TimedRotatingFileHandler
__loghandle = TimedRotatingFileHandler(os.path.join(os.getcwd(), 'covguard.log'), when='D', interval=1, backupCount=5)
__loghandle.setFormatter( logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') )
logging.root.addHandler(__loghandle)


# setup sites
##import site
##__sites_path = os.path.join(os.getcwd(), 'sites//')
##logging.info(__sites_path)
##if os.path.exists(__sites_path):
##	site.addsitedir(__sites_path)
##else:
##	logging.warn("%s does not exists!",__sites_path)

# check sites
import tornado
import tornado.ioloop
import tornado.web

import subprocess
# boot server
import io_udp_server
import io_config
import io_db
import io_app

import multiprocessing

def boot():

    print "1. load memory database server"

    # load memory database server
    io_db.openShareDB(io_config.settings['db_path'], io_config.settings['db_name'])


    #print "2. boot io udp server"
    # boot io udp server
    #io_udp_server.run(io_config.settings['host'], io_config.settings['port'])


    print "3. boot app server"
    # boot app server
    io_app.run()

if __name__ == '__main__':
    boot()
