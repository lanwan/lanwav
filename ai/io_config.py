#-------------------------------------------------------------------------------
# Name:        io_config.py
# Purpose:
#
# Author:      Steven.ZDWang
#
# Created:     24/10/2017
# Copyright:   (c) Steven.ZDWang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import logging
import os

debug = 1

settings = {}

settings['host'] = "0.0.0.0"
if debug:
    settings['port']  = 9100
else:
    settings['port']  = 9800

settings['db_path'] = os.getcwd()

settings['webport'] = 8090

def main():
    pass

if __name__ == '__main__':
    main()
