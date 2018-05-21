import sys, pexpect
from time import sleep
from time import time
import struct
import binascii

file = open('atmo_history.txt', 'w')
file.close()

def saveData(data): 
    file = open('atmo_history.txt', 'a')
    file.write(data)
    file.close()
    print(data)

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
##time_bytes = struct.pack(">i", time_ts)

sendlist = name_bytes + time_ts.to_bytes(4, byteorder = 'big')

##name_const = 'const'
##name_bytes = name_const.encode('ASCII')

##send_name = ''
for x in sendlist:
    print(x)
##    send_name = send_name + str(int(x))
cmd = 'const'.encode('ASCII')
gatt.sendline('char-write-req 0x0011 %s' % ''.join(format(x, '02x') for x in sendlist))       
##print(send_name)
##gatt.send('char-write-req 0x0011 ' + str(sendlist))
##gatt.expect('Characteristic value was written successfully')
##print('Send sync ok')
##
while True:
    gatt.expect('value.*', timeout=1000)
    param = gatt.after
    print(param)
##    param = int(param.split()[2], 16)
##    data = '\nVOC: ' + str(param) + ' Time: ' + time()
##    saveData(data)
 
    
    
##    name_str = 'ERR'
##    name_bytes = name_str.encode('ASCII')
##    gatt.expect(name_bytes, timeout=1000)
##    print('ERR')
##    param = gatt.after
##    param = int(param.split()[0])
##    print(param)

##while True:
##    gatt.expect('value.*', timeout=1000)
##    param = gatt.after
##    saveData(str(param))




