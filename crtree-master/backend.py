#!/usr/bin/env python

from random import randint
from flask import Flask, send_from_directory, jsonify
import sys, pexpect
from time import sleep
from time import time
import struct
import binascii

app = Flask(__name__, static_url_path='/static')
value = 0
gatt=pexpect.spawn('gatttool -t random -b C6:E9:37:EC:21:35 -I')

@app.route('/', methods=['GET'])
def home():
    global gatt
    gatt.logfile = open("/tmp/mylog", "wb")
    gatt.sendline('connect')
    gatt.expect('Connection successful') 
    print("success gatt notice!")

    #enable notice
    gatt.sendline('char-write-req 0x000f 0100')
    gatt.expect('Characteristic value was written successfully')
    print("Notice enable")

    #send sync time
    name_str = 'HST'
    name_bytes = name_str.encode('ASCII')
    time_ts = int(time())
    sendlist = name_bytes + time_ts.to_bytes(4, byteorder = 'big')
    cmd = 'const'.encode('ASCII')
    gatt.sendline('char-write-req 0x0011 %s' % ''.join(format(x, '02x') for x in sendlist))       
    
    return send_from_directory('static', 'index.html')

@app.route('/trash_counter', methods=['GET'])
def trash_counter():
##    global value
##    value += randint(0, 100)
    global gatt
    gatt.expect('value.*', timeout=1000)
    param = gatt.after
    return jsonify({'value': param})


if __name__ == '__main__':
    app.run(debug=True)
