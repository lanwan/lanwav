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

import datetime
import time
import sqlite3
class IOTSQLite3DB:
    def __init__(self, dbname):

        self.__realtime_ds = {}
        self.__live_users = {}
        self.__conn = sqlite3.connect(dbname)
        pass

    def __del__(self):

        if self.__conn:
            self.__conn.close()

        pass

    def verify_user(self, login_name, pwd):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        c.execute("select role_id from t_user where user_id = '%s' and pwd = '%s'" % (login_name, pwd))
        r = c.fetchone()
        if r:
            login_time = time.strftime("%Y-%m-%d %H:%M:%S")
            c.execute("update t_user set login_time = ? where user_id = ?", (login_time, login_name) )
            self.__conn.commit()
            c.close()
            return r[0]
        else:
            c.close()
            return False

    def get_user(self, login_name):
        if not self.__conn:
            return

        c = self.__conn.cursor()
        c.execute("select * from t_user where user_id = '%s'" % login_name)
        res = c.fetchone()
        c.close()
        return res


    def add_user(self, login_name, user_name, pwd, city, telphone):
        if not self.__conn:
            return False

        reg_time = time.strftime("%Y-%m-%d %H:%M:%S")
        c = self.__conn.cursor()
        try:
            c.execute("insert into t_user(user_id, user_name, pwd, city, telphone, reg_time) values (?,?,?,?,?,?) ",
                (login_name, user_name, pwd, city, telphone, reg_time))
            self.__conn.commit()
            c.close()
            return True
        except:
            c.close()
            return False


    def remove_user(self, login_name):
        return

    def add_live_data(self, data):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        try:
            c.execute("insert into t_livedata(live_id, station_id, rcv_time, voltage, signal, attitude, att_x, att_y, att_z) values (?,?,?,?,?,?,?,?,?) ",
                (data.live_id, data.station_id, data.rcv_time, data.voltage, data.signal, data.attitude, data.att_x, data.att_y, data.att_z))
            self.__conn.commit()
            c.close()
            return True
        except:
            c.close()
            return False

    def get_station_dataset(self, role_id):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        c.execute("select * from t_station where role_key like '%,role_id,%'")
        return c.fetchall()

    def get_alert_dataset(self, station_id):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        c.execute("select * from t_alert where station_id == ? order by alert_time desc", (station_id) )
        return c.fetchall()

    def set_alert_opts(self, station_id, opts):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        try:
            c.execute("insert into t_alertcfg(station_id, opts) values (?, ?) ",(station_id, opts))
            self.__conn.commit()
            c.close()
            return False
        except:
            try:
                c.execute("update t_alertcfg set opts = ? where station_id == ?",(opts, station_id))
                self.__conn.commit()
                c.close()
                return True
            except:
                c.close()
                return False


    def get_alert_opts(self, station_id):
        if not self.__conn:
            return False

        c = self.__conn.cursor()
        c.execute("select * from t_alertcfg where station_id == ?", (station_id) )
        return c.fetchone()


__db = None
def getShareDB():
    global __db
    return __db

def openShareDB(path, name):
    global __db
    __db = IOTSQLite3DB( os.path.join(path, name))

def test():
    db = IOTSQLite3DB("./covg.db3")
    print db.verify_user('wzd', '588')

    #print db.add_user('test_1233', 'test', '2222', 'jiaxing', '15825707488')
    print db.set_alert_opts('1', '1')
    pass

if __name__ == '__main__':
    test()
