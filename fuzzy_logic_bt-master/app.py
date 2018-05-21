import json
from time import time
import serial
from flask import Flask, render_template, make_response
import bluetoothSync
from random import random
import sys, pexpect
from time import sleep
import struct
import binascii

##port="/dev/tty.HC-05-DevB" #This will be different for various devices and on windows it will probably be a COM port.
##bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
##bluetooth.flushInput() #This gives the bluetooth a little kick

file = open('atmo_history.txt', 'w')
file.close()

gatt=pexpect.spawn('gatttool -t random -b DA:A3:03:1C:41:05 -I')
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

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

@app.route('/live-data')
def live_data():
    data = [time() * 1000, random() * 100]
    print('>>>data:' + data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
