'''
Author: Rick rick@guaik.io
Date: 2023-01-10 13:48:15
LastEditors: Rick rick@guaik.io
LastEditTime: 2023-01-10 22:38:40
FilePath: \BilibiliUserInfo\PyBilibiliUserInfo.py
Description: 
Copyright (c) 2023 by Rick email: rick@guaik.io, All Rights Reserved.
'''
# coding=utf-8

import urllib.request
from ctypes import *
import json
import serial
import time

UID = "358330282"
COM = "COM11"
STA_URL = "https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp" % UID

fields_list = [("following", c_int32),
               ("follower", c_int32)]


class STAStruct(LittleEndianStructure):
    _fields_ = fields_list
    _pack_ = 1  # 按照1字节对齐


if __name__ == "__main__":
    ser = serial.Serial()
    ser.port = COM  # 设置端口号
    ser.baudrate = 115200  # 设置波特率
    ser.bytesize = 8  # 设置数据位
    ser.stopbits = 1  # 设置停止位
    ser.parity = "N"  # 设置校验位
    ser.timeout = 1
    ser.open()
    if (not ser.isOpen()):
        exit(-1)
    print("serial: %s open success..." % COM)

    while True:
        sta_response = urllib.request.urlopen(STA_URL)
        j_data = sta_response.read()
        print(j_data)
        d = json.loads(j_data)
        value_list = [c_int32(d['data']['following']),
                      c_int32(d['data']['follower'])]
        obj = STAStruct(*value_list)
        print("following: %d follower: %d" % (obj.following, obj.follower))
        buffer = (c_ubyte*sizeof(STAStruct))()
        memmove(buffer, byref(obj), sizeof(STAStruct))
        ser.write(buffer)
        time.sleep(3)
