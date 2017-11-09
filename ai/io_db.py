#-------------------------------------------------------------------------------
# Name:        db_server.py
# Purpose:
#
# Author:      Steven.ZDWang
#
# Created:     24/10/2017
# Copyright:   (c) Steven.ZDWang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
    db_station[station_id] = [status, time, region_id, name, gps_lat, gps_lon, x, y, z, battery voltage, wireless signal]
    db_station["1001"] = [0, 2017-10-24 14:25:35, "222", Shimao", x, y, z, 3.6, 20]
    db_alert[1] = ["1001", "1002"]
    db_alert[2] = ["1001", "1002"]
    db_alert[3] = ["1001", "1002"]
    db_users{} = {'lname':[id, pwd]}
'''


import os
import logging
import cPickle


dbserver = None


class IOTDBServer:
    def  __init__(self, path, name):
        self.db_station = {}
        self.db_alert = {}
        self.db_users = {}
        self.db_users['wzd'] = ['wzd', '588']

        self.name = name
        self.dbpath = os.path.join(path, name)
        if not os.path.exists(self.dbpath):
            os.makedirs(self.dbpath)
        self.station_filename = os.path.join(self.dbpath, "station.pob")
        self.alert_filename = os.path.join(self.dbpath, "alert.pob")
        self.users_filename = os.path.join(self.dbpath, "users.pob")
        logging.info("station file name: ", self.station_filename)
        logging.info("alert file name: ", self.alert_filename)

    def save(self):
        with closing(open(self.station_filename,'wb')) as f:
            cPickle.dump(self.db_station, f)

        with closing(open(self.alert_filename,'wb')) as f:
            cPickle.dump(self.db_alert, f)


    def load(self):
        if os.path.exists(self.station_filename):
            with closing(open(self.station_filename,'rb')) as f:
                self.db_station = cPickle.load(f)

        if os.path.exists(self.alert_filename):
            with closing(open(self.alert_filename,'rb')) as f:
                self.db_alert = cPickle.load(self.alert_filename)

        if os.path.exists(self.users_filename):
            with closing(open(self.users_filename,'rb')) as f:
                self.db_users = cPickle.load(self.users_filename)

    def verify(self, userid, pwd):
        if userid and  self.db_users.has_key(userid):
            return self.db_users[userid]

def test():
    pass

if __name__ == '__main__':
    test()
