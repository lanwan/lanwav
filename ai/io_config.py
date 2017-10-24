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
import io_boot

debug = 0

io_setttins['host'] = "0.0.0.0"
if io_boot.debug:
    io_setttins['port']  = 9100
else:
    io_setttins['port']  = 9800


def main():
    pass

if __name__ == '__main__':
    main()
