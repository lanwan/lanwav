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

import logging
import io_udp_server
import io_config

def main():
    io_udp_server.run_udp_server(io_config.io_setttins['host'], io_config.io_setttins['port'])

if __name__ == '__main__':
    main()
